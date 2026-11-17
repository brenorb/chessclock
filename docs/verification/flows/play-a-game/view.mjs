export const title = "Play a timed game";
export const state = (v) => ({
  setup: "Set the game time",
  running: v.turn === 1 ? "Player 1's clock running" : "Player 2's clock running",
  paused: "Paused",
  over: "Time's up",
}[v.screen]);
const steps = {
  YouStart: "you press start",
  SecondPasses: "the game time runs out",
  PlayerMoves: "the player taps their clock",
  YouPause: "you pause",
  YouResume: "you resume",
  YouReset: "you reset",
};
export const step = (action, from, to) =>
  action === "SecondPasses" ? (to.screen === "over" ? "the game time runs out" : null) : (steps[action] ?? null);
export const group = (v) => (v.screen === "over" ? "done" : v.screen === "setup" ? "idle" : "playing");
export const colors = { done: "orange", idle: "tan", playing: "blue" };
