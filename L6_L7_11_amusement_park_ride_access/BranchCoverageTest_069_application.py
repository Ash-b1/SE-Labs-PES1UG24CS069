from CodeCoverageTest_069_application import *  # noqa: F401,F403 (reuse all line-coverage tests)
from CodeCoverageTest_069_application import grp, p
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints


# ---- extra tests aimed at the remaining branches ----
def test_empty_groups_list_skips_loop():
    assert process_ride_admissions([], 5.0) == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_open_group_with_no_patrons_skips_inner_loop():
    r = process_ride_admissions([grp(patrons=[])], 5.0)
    assert r["status"] == "ZERO_ADMISSIONS"


def test_fast_lane_only_revenue_when_no_patrons():
    r = process_ride_admissions([grp(patrons=[], fast=True)], 5.0)
    assert r == {"total_revenue": 5.0, "status": "COMPLETED"}


def test_exactly_four_rejections_not_audit():
    r = process_ride_admissions([grp(patrons=[p(h=100)] * 4 + [p()])], 0)
    assert r["status"] == "COMPLETED"


def test_height_boundary_120_admitted():
    assert process_ride_admissions([grp(patrons=[p(h=120)])], 0)["total_revenue"] == 10.0


def test_zero_fee_allowed():
    assert process_ride_admissions([], 0)["status"] == "ZERO_ADMISSIONS"


def test_multiple_groups_mixed():
    groups = [grp("roller_coaster", [p()]), grp(open_=False), grp("water_ride", [p(child=True)], fast=True)]
    r = process_ride_admissions(groups, 2.0)
    assert r == {"total_revenue": 25.0 + 10.8 + 2.0, "status": "COMPLETED"}


def test_restraints_all_latched_safe():
    assert inspect_safety_restraints([[1, 1, 1], [1]]) == "SAFE"


def test_restraints_empty_sensor_stream_inner_loop_skipped():
    assert inspect_safety_restraints([[]]) == "SAFE"


def test_restraints_single_zero_does_not_lock():
    assert inspect_safety_restraints([[0]]) == "SAFE"


def test_restraints_streak_resets_between_streams():
    assert inspect_safety_restraints([[1, 0], [0, 1]]) == "SAFE"


def test_restraints_lock_in_second_stream():
    assert inspect_safety_restraints([[1, 1], [0, 0]]) == "EMERGENCY_LOCK"