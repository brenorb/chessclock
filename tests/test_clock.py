import unittest
from unittest.mock import patch

import main


class ClockTests(unittest.TestCase):
    def setUp(self):
        self.client = main.app.test_client()
        self.addCleanup(self.client.get, "/reset")
        clock = patch.object(main.time, "time", return_value=100)
        self.now = clock.start()
        self.addCleanup(clock.stop)
        self.client.get("/reset")
        self.assertEqual(self.client.post("/set_global_time", json={"time": 60}).status_code, 200)
        self.assertEqual(self.client.get("/start").status_code, 200)

    def test_pause_and_resume_keep_the_remaining_time(self):
        self.now.return_value = 112
        switched = self.client.get("/switch/2").get_json()
        self.assertEqual(switched["player1_time"], 12)

        self.now.return_value = 118
        paused = self.client.get("/pause").get_json()
        self.assertEqual(paused["player2_time"], 6)
        self.assertEqual(paused["global_time"], 42)

        self.now.return_value = 130
        self.assertEqual(self.client.get("/state").get_json(), paused)
        self.assertFalse(self.client.get("/pause").get_json()["is_paused"])

        self.now.return_value = 175
        expired = self.client.get("/state").get_json()
        self.assertEqual(expired["global_time"], 0)
        self.assertEqual(expired["player2_time"], 48)
        self.now.return_value = 180
        self.assertEqual(self.client.get("/state").get_json(), expired)
        self.assertEqual(self.client.get("/start").get_json(), expired)
        self.assertEqual(self.client.get("/reset").get_json()["global_time"], 60)
        self.assertEqual(self.client.get("/start").get_json()["active_player"], 1)

    def test_pause_or_switch_cannot_pass_an_unpolled_deadline(self):
        for route in ("/pause", "/switch/2"):
            with self.subTest(route=route):
                self.now.return_value = 100
                self.client.get("/reset")
                self.client.get("/start")
                self.now.return_value = 165
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)
                state = response.get_json()
                self.assertEqual(state["global_time"], 0)
                self.assertEqual(state["player1_time"], 60)
                self.assertEqual(state["player2_time"], 0)
                self.assertEqual(state["active_player"], 1)
                self.assertFalse(state["is_paused"])
                self.assertEqual(self.client.get("/state").get_json(), state)

    def test_invalid_player_does_not_change_the_active_player(self):
        self.assertEqual(self.client.get("/switch/3").status_code, 400)
        self.assertEqual(self.client.get("/state").get_json()["active_player"], 1)
