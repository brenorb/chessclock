"""Replays of the Clock.tla rules on the real Flask routes in main.py."""

import pytest

import main


@pytest.fixture
def clock(monkeypatch):
    now = {"t": 1000.0}
    monkeypatch.setattr(main.time, "time", lambda: now["t"])
    client = main.app.test_client()
    client.get("/reset")
    client.post("/set_global_time", json={"time": 60})

    def advance(seconds):
        now["t"] += seconds

    return client, advance


def totals(state):
    return state["player1_time"] + state["player2_time"] + state["global_time"]


def test_switch_rejects_a_player_that_does_not_exist(clock):
    client, advance = clock
    client.get("/start")
    assert client.get("/switch/3").status_code == 400
    advance(10)
    state = client.get("/state").get_json()
    assert state["active_player"] == 1
    assert totals(state) == pytest.approx(60)


def test_start_refuses_to_restart_a_running_game(clock):
    client, advance = clock
    client.get("/start")
    advance(20)
    client.get("/state")
    assert client.get("/start").status_code == 400
    assert totals(client.get("/state").get_json()) == pytest.approx(60)


def test_the_clock_stops_at_zero(clock):
    client, advance = clock
    client.get("/start")
    advance(45)
    client.get("/switch/2")
    advance(30)
    state = client.get("/state").get_json()
    assert state["global_time"] == 0
    assert state["finished"] is True
    assert state["player1_time"] == pytest.approx(45)
    assert state["player2_time"] == pytest.approx(15)
    assert client.get("/switch/1").status_code == 400
