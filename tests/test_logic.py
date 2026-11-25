"""Tests for the pure rules: combat maths, items and room progression.

Run from the project root:
    python -m unittest discover tests
"""

import math
import unittest

import combat
import items
import progression


class SpreadAnglesTest(unittest.TestCase):
    def test_single_projectile_keeps_the_aim(self):
        self.assertEqual(combat.spread_angles(90.0, 1, 18.0), [90.0])

    def test_three_projectiles_are_symmetric_around_the_aim(self):
        angles = combat.spread_angles(90.0, 3, 18.0)
        self.assertAlmostEqual(angles[0], 81.0)
        self.assertAlmostEqual(angles[1], 90.0)
        self.assertAlmostEqual(angles[2], 99.0)

    def test_the_middle_projectile_always_uses_the_aim(self):
        for count in (1, 3, 5, 7):
            angles = combat.spread_angles(0.0, count, 20.0)
            self.assertAlmostEqual(angles[count // 2], 0.0)


class CircleOverlapTest(unittest.TestCase):
    def test_touching_circles_overlap(self):
        self.assertTrue(combat.circle_overlap(0.0, 0.0, 5.0, 10.0, 0.0, 5.0))

    def test_circles_one_pixel_apart_do_not_overlap(self):
        self.assertFalse(combat.circle_overlap(0.0, 0.0, 5.0, 10.1, 0.0, 5.0))

    def test_a_small_circle_inside_a_big_one_overlaps(self):
        self.assertTrue(combat.circle_overlap(0.0, 0.0, 30.0, 4.0, 4.0, 2.0))


class DamageTest(unittest.TestCase):
    def test_armour_never_produces_negative_damage(self):
        self.assertEqual(combat.damage_after_armour(1.0, 5.0), 0.0)

    def test_armour_reduces_damage(self):
        self.assertAlmostEqual(combat.damage_after_armour(2.0, 0.5), 1.5)


class ClampTest(unittest.TestCase):
    def test_an_inside_position_is_unchanged(self):
        self.assertEqual(
            combat.clamp_to_rect(100.0, 100.0, 10.0, 0.0, 0.0, 200.0, 200.0),
            (100.0, 100.0))

    def test_a_position_outside_is_pulled_back_by_the_radius(self):
        self.assertEqual(
            combat.clamp_to_rect(-50.0, 400.0, 10.0, 0.0, 0.0, 200.0, 200.0),
            (10.0, 190.0))

    def test_a_rectangle_smaller_than_the_body_uses_its_centre(self):
        self.assertEqual(
            combat.clamp_to_rect(0.0, 0.0, 50.0, 0.0, 0.0, 40.0, 40.0),
            (20.0, 20.0))


class AngleTest(unittest.TestCase):
    def test_up_is_negative_y_on_screen(self):
        dx, dy = combat.direction_from_angle(90.0)
        self.assertAlmostEqual(dx, 0.0)
        self.assertAlmostEqual(dy, -1.0)

    def test_direction_and_angle_round_trip(self):
        for degrees in (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0):
            dx, dy = combat.direction_from_angle(degrees)
            result = combat.angle_from_direction(dx, dy)
            # Angles are the same when they differ by a full turn.
            difference = (result - degrees + 180.0) % 360.0 - 180.0
            self.assertAlmostEqual(difference, 0.0, places=6)

    def test_a_zero_length_direction_is_safe(self):
        self.assertEqual(combat.unit_vector(0.0, 0.0), (0.0, 0.0))


class PierceTest(unittest.TestCase):
    def test_infinite_pierce_never_runs_out(self):
        self.assertEqual(
            combat.consume_pierce(combat.INFINITE_PIERCE),
            combat.INFINITE_PIERCE)
        self.assertFalse(combat.is_spent(combat.INFINITE_PIERCE))

    def test_one_pierce_is_spent_after_a_hit(self):
        self.assertTrue(combat.is_spent(combat.consume_pierce(1)))

    def test_two_pierce_survives_one_hit(self):
        remaining = combat.consume_pierce(2)
        self.assertFalse(combat.is_spent(remaining))
        self.assertTrue(combat.is_spent(combat.consume_pierce(remaining)))


class HealthRatioTest(unittest.TestCase):
    def test_half_health_is_half(self):
        self.assertAlmostEqual(combat.health_ratio(3, 6), 0.5)

    def test_a_zero_maximum_is_safe(self):
        self.assertEqual(combat.health_ratio(3, 0), 0.0)

    def test_the_ratio_is_clamped(self):
        self.assertEqual(combat.health_ratio(12, 6), 1.0)
        self.assertEqual(combat.health_ratio(-1, 6), 0.0)


class AttackStatsTest(unittest.TestCase):
    def test_replace_returns_a_new_object(self):
        base = combat.base_attack()
        changed = base.replace(damage=5.0)
        self.assertIsNot(base, changed)
        self.assertEqual(base.damage, 1.0)
        self.assertEqual(changed.damage, 5.0)

    def test_equality_compares_every_field(self):
        self.assertEqual(combat.base_attack(), combat.base_attack())
        self.assertNotEqual(combat.base_attack(), combat.base_attack().replace(
            cooldown=9.0))


class ApplyItemTest(unittest.TestCase):
    def assertStats(self, stats, damage, cooldown, pierce, projectiles, spread):
        self.assertAlmostEqual(stats.damage, damage)
        self.assertAlmostEqual(stats.cooldown, cooldown)
        self.assertEqual(stats.pierce, pierce)
        self.assertEqual(stats.projectiles, projectiles)
        self.assertAlmostEqual(stats.spread, spread)

    def test_gauntlet_doubles_damage_and_cooldown(self):
        stats = items.apply_item(combat.base_attack(), items.GAUNTLET)
        self.assertStats(stats, 2.0, 0.52, 1, 1, 0.0)

    def test_laser_pierces_everything_for_half_damage(self):
        stats = items.apply_item(combat.base_attack(), items.LASER)
        self.assertStats(stats, 0.5, 0.286, combat.INFINITE_PIERCE, 1, 0.0)

    def test_triplegun_fires_three_faster_weaker_tears(self):
        stats = items.apply_item(combat.base_attack(), items.TRIPLEGUN)
        self.assertStats(stats, 0.6, 0.169, 1, 3, 18.0)

    def test_the_original_stats_are_never_changed(self):
        base = combat.base_attack()
        snapshot = base.replace()
        for item in items.ITEM_ORDER:
            items.apply_item(base, item)
        self.assertEqual(base, snapshot)

    def test_two_items_compound(self):
        once = items.apply_item(combat.base_attack(), items.GAUNTLET)
        twice = items.apply_item(once, items.GAUNTLET)
        self.assertAlmostEqual(twice.damage, 4.0)
        self.assertAlmostEqual(twice.cooldown, 1.04)

    def test_a_laser_after_a_gauntlet_keeps_infinite_pierce(self):
        stats = items.apply_item(
            items.apply_item(combat.base_attack(), items.GAUNTLET),
            items.LASER)
        self.assertEqual(stats.pierce, combat.INFINITE_PIERCE)
        self.assertAlmostEqual(stats.damage, 1.0)

    def test_there_are_exactly_three_items(self):
        self.assertEqual(len(items.ITEM_ORDER), 3)
        self.assertEqual(len({item.key for item in items.ITEM_ORDER}), 3)


class ProgressionTest(unittest.TestCase):
    def test_the_gauntlet_has_five_rooms(self):
        self.assertEqual(progression.total_rooms(), 5)

    def test_rooms_walk_in_order(self):
        walked = [progression.ROOM_ORDER[0]]
        while True:
            following = progression.next_room(walked[-1])
            if following is None:
                break
            walked.append(following)
        self.assertEqual(tuple(walked), progression.ROOM_ORDER)

    def test_the_boss_is_the_last_room(self):
        self.assertIsNone(progression.next_room(progression.ROOM_BOSS))

    def test_room_numbers_start_at_one(self):
        self.assertEqual(progression.room_number(progression.ROOM_TUTORIAL), 1)
        self.assertEqual(progression.room_number(progression.ROOM_BOSS), 5)

    def test_the_tutorial_door_is_open_with_enemies_present(self):
        self.assertTrue(progression.door_is_open(
            progression.ROOM_TUTORIAL, enemies_remaining=5, item_taken=False))

    def test_a_mob_room_blocks_while_enemies_live(self):
        self.assertFalse(progression.door_is_open(
            progression.ROOM_MOB_ONE, enemies_remaining=3, item_taken=False))

    def test_a_mob_room_opens_when_cleared(self):
        self.assertTrue(progression.door_is_open(
            progression.ROOM_MOB_ONE, enemies_remaining=0, item_taken=False))

    def test_the_item_room_blocks_until_an_item_is_taken(self):
        self.assertFalse(progression.door_is_open(
            progression.ROOM_ITEM, enemies_remaining=0, item_taken=False))
        self.assertTrue(progression.door_is_open(
            progression.ROOM_ITEM, enemies_remaining=0, item_taken=True))

    def test_the_boss_door_opens_only_after_the_boss_dies(self):
        self.assertFalse(progression.door_is_open(
            progression.ROOM_BOSS, enemies_remaining=1, item_taken=False))
        self.assertTrue(progression.door_is_open(
            progression.ROOM_BOSS, enemies_remaining=0, item_taken=False))


class BossPhaseTest(unittest.TestCase):
    def test_full_health_is_phase_one(self):
        self.assertEqual(progression.boss_phase(1.0), 1)

    def test_just_above_sixty_percent_is_still_phase_one(self):
        self.assertEqual(progression.boss_phase(0.601), 1)

    def test_sixty_percent_is_phase_two(self):
        self.assertEqual(progression.boss_phase(0.60), 2)

    def test_thirty_one_percent_is_phase_two(self):
        self.assertEqual(progression.boss_phase(0.31), 2)

    def test_thirty_percent_is_phase_three(self):
        self.assertEqual(progression.boss_phase(0.30), 3)

    def test_zero_health_is_phase_three(self):
        self.assertEqual(progression.boss_phase(0.0), 3)


class EnemyHealthTest(unittest.TestCase):
    """Enemy hit points come from settings, so the numbers stay in one place."""

    def test_every_enemy_needs_more_than_one_base_tear(self):
        import settings
        for hp in (settings.BLOB_HP, settings.CUBE_HP,
                   settings.SPIDER_HP, settings.BOSS_HP):
            self.assertGreater(hp, settings.BASE_DAMAGE)

    def test_the_boss_takes_the_longest_to_kill(self):
        import settings
        others = (settings.BLOB_HP, settings.CUBE_HP, settings.SPIDER_HP)
        self.assertGreater(settings.BOSS_HP, max(others))

    def test_a_gauntlet_hit_still_needs_a_sane_number_of_tears(self):
        import settings
        stats = items.apply_item(combat.base_attack(), items.GAUNTLET)
        tears_needed = math.ceil(settings.BOSS_HP / stats.damage)
        self.assertGreater(tears_needed, 10)
        self.assertLess(tears_needed, 60)


if __name__ == "__main__":
    unittest.main()
