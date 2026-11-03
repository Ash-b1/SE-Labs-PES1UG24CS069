import pytest
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints


def grp(ride="family", patrons=None, open_=True, fast=False):
    return {"is_open": open_, "ride_type": ride, "has_fast_lane": fast,
            "patrons": patrons if patrons is not None else []}


def p(h=150, warn=False, child=False):
    return {"height_cm": h, "health_warning": warn, "is_child": child}


# ---------- process_ride_admissions ----------
def test_single_adult_family_ride():
    r = process_ride_admissions([grp(patrons=[p()])], 5.0)
    assert r == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_invalid_groups_not_list():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)


def test_invalid_negative_fee():
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_closed_group_skipped():
    r = process_ride_admissions([grp(open_=False, patrons=[p()])], 5.0)
    assert r["status"] == "ZERO_ADMISSIONS"


def test_roller_coaster_adult():
    r = process_ride_admissions([grp("roller_coaster", [p()])], 0)
    assert r["total_revenue"] == 25.0


def test_water_ride_child_discount():
    r = process_ride_admissions([grp("water_ride", [p(child=True)])], 0)
    assert r["total_revenue"] == 10.8  # 18 * 0.6


def test_unknown_ride_type_rejected():
    r = process_ride_admissions([grp("bumper_cars", [p()])], 0)
    assert r["status"] == "ZERO_ADMISSIONS"


def test_default_ride_type_is_family():
    g = {"is_open": True, "patrons": [p()]}  # no ride_type key
    assert process_ride_admissions([g], 0)["total_revenue"] == 10.0


def test_invalid_height_rejected():
    r = process_ride_admissions([grp(patrons=[p(h=0)])], 0)
    assert r["status"] == "ZERO_ADMISSIONS"


def test_too_short_rejected():
    r = process_ride_admissions([grp(patrons=[p(h=119)])], 0)
    assert r["status"] == "ZERO_ADMISSIONS"


def test_health_warning_family_ride_continues():
    r = process_ride_admissions([grp(patrons=[p(warn=True), p()])], 0)
    assert r["total_revenue"] == 10.0  # warned patron rejected, next admitted


def test_health_warning_roller_coaster_cancels_group():
    r = process_ride_admissions([grp("roller_coaster", [p(), p(warn=True), p()])], 0)
    assert r["status"] == "ZERO_ADMISSIONS"  # group_total reset + break


def test_fast_lane_fee_added():
    r = process_ride_admissions([grp(patrons=[p()], fast=True)], 5.0)
    assert r["total_revenue"] == 15.0


def test_safety_audit_more_than_four_rejections():
    r = process_ride_admissions([grp(patrons=[p(h=100)] * 5 + [p()])], 0)
    assert r == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}


# ---------- inspect_safety_restraints ----------
def test_restraints_no_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_restraints_emergency_lock():
    assert inspect_safety_restraints([[1, 0, 0]]) == "EMERGENCY_LOCK"


def test_restraints_streak_reset_then_safe():
    assert inspect_safety_restraints([[0, 1, 0, 1]]) == "SAFE"