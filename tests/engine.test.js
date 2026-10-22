// Run: node tests/engine.test.js
'use strict';
var assert = require('assert');
var E = require('../web/engine.js');
var AI = require('../web/ai.js');

var passed = 0;
function test(name, fn) {
  try { fn(); passed++; }
  catch (e) { console.error('FAIL ' + name + '\n  ' + (e && e.stack || e)); process.exitCode = 1; }
}

function c(r, s) { return { r: r, s: s, id: r + s.charAt(0) }; }

// A game with a hand-built board.
function board(subjects) {
  var s = E.newGame({ seed: 1 });
  E.SEATS.forEach(function (seat) {
    E.POS.forEach(function (p, i) { s.courts[seat].subjects[p] = subjects[seat][i]; });
  });
  E.LANES.forEach(function (l) { s.lanes[l.id] = { paired: false, gem: false, spawnTurn: 0 }; });
  E.SEATS.forEach(function (seat) { s.flush[seat] = { on: false, spawnTurn: 0 }; });
  return s;
}

test('trump: ranks cycle K>Q>J>K', function () {
  assert.strictEqual(E.trump(c('K', 'spades'), c('Q', 'clubs')), 1);
  assert.strictEqual(E.trump(c('Q', 'spades'), c('J', 'clubs')), 1);
  assert.strictEqual(E.trump(c('J', 'spades'), c('K', 'clubs')), 1);
  assert.strictEqual(E.trump(c('Q', 'hearts'), c('K', 'spades')), -1);
});

test('trump: suits cycle on equal rank, same colour stalemates', function () {
  assert.strictEqual(E.trump(c('K', 'spades'), c('K', 'hearts')), 1);
  assert.strictEqual(E.trump(c('K', 'hearts'), c('K', 'clubs')), 1);
  assert.strictEqual(E.trump(c('K', 'clubs'), c('K', 'diamonds')), 1);
  assert.strictEqual(E.trump(c('K', 'diamonds'), c('K', 'spades')), 1);
  assert.strictEqual(E.trump(c('K', 'spades'), c('K', 'clubs')), 0);
  assert.strictEqual(E.trump(c('K', 'hearts'), c('K', 'diamonds')), 0);
});

test('pairs: equal ranks, aces wild', function () {
  assert(E.isPair(c('7', 'spades'), c('7', 'hearts')));
  assert(E.isPair(c('A', 'spades'), c('7', 'hearts')));
  assert(E.isPair(c('A', 'spades'), c('A', 'hearts')));
  assert(!E.isPair(c('6', 'spades'), c('7', 'hearts')));
});

test('deal: 12 subjects, 28 in the deck, royals J/K/Q, one free action', function () {
  var s = E.newGame({ seed: 'x' });
  assert.strictEqual(s.deck.length, 28);
  E.SEATS.forEach(function (seat) {
    assert.strictEqual(s.courts[seat].royals.L.r, 'J');
    assert.strictEqual(s.courts[seat].royals.C.r, 'K');
    assert.strictEqual(s.courts[seat].royals.R.r, 'Q');
  });
  assert.strictEqual(s.free, 1);
  assert.strictEqual(s.current, 'S');
});

test('opening control: right corner, ridges by suit, peaks stalemated', function () {
  var s = E.newGame({ seed: 2 });
  assert.strictEqual(E.controller(s, 'cSE'), 'S'); // S.R Queen beats E.L Jack
  assert.strictEqual(E.controller(s, 'cWS'), 'W');
  assert.strictEqual(E.controller(s, 'rSE'), 'S'); // K spades beats K hearts
  assert.strictEqual(E.controller(s, 'rWS'), 'W'); // K diamonds beats K spades
  assert.strictEqual(E.controller(s, 'pSN'), null); // K spades vs K clubs
  assert.strictEqual(E.controller(s, 'pEW'), null);
});

test('own lane: only the controller may swap', function () {
  var s = E.newGame({ seed: 3 });
  assert.strictEqual(E.laneAccess(s, 'cSE', 'S').ok, true);
  assert.strictEqual(E.laneAccess(s, 'cWS', 'S').ok, false); // W controls
  assert.strictEqual(E.laneAccess(s, 'pSN', 'S').ok, false); // stalemate
});

test('foreign lane: pay the controller', function () {
  var s = E.newGame({ seed: 4 });
  var acc = E.laneAccess(s, 'cEN', 'S');
  assert.strictEqual(acc.ok, true);
  assert.strictEqual(acc.toll, 'E');
  var r = E.apply(s, { type: 'lane', lane: 'cEN' });
  assert(!r.error, r.error);
  assert.strictEqual(r.state.players.E.gems >= 1, true);
  assert.strictEqual(r.state.free, 0);
});

test('court swap is free of control and costs the free action', function () {
  var s = E.newGame({ seed: 5 });
  var L = s.courts.S.subjects.L.id, C = s.courts.S.subjects.C.id;
  var r = E.apply(s, { type: 'court', a: 'L', b: 'C' });
  assert.strictEqual(r.state.courts.S.subjects.L.id, C);
  assert.strictEqual(r.state.courts.S.subjects.C.id, L);
  assert.strictEqual(r.state.free, 0);
  var r2 = E.apply(r.state, { type: 'court', a: 'L', b: 'C' });
  assert(r2.error, 'second action with no gems should fail');
});

test('making a pair spawns a gem; the controller collects it at once', function () {
  var s = board({
    S: [c('2', 'hearts'), c('3', 'hearts'), c('9', 'clubs')],
    E: [c('5', 'clubs'), c('4', 'diamonds'), c('6', 'diamonds')],
    N: [c('7', 'hearts'), c('8', 'diamonds'), c('2', 'spades')],
    W: [c('3', 'clubs'), c('6', 'spades'), c('4', 'spades')]
  });
  // S swaps L and R: S.R becomes 2... we want S.R to pair E.L (5): swap S.R with nothing.
  // Instead S swaps across its own corner cSE (S controls it): S.R=9, E.L=5 -> no pair.
  // Swap S.L<->S.C to make no pair, then check rSE: S.C=3 vs E.C=4 no.
  s.courts.S.subjects.R = c('5', 'spades');
  var before = s.players.S.gems;
  // Pair cSE by swapping S.L and S.R? Build it directly: S.L=5? Use a court swap.
  s.courts.S.subjects.L = c('5', 'hearts');
  s.courts.S.subjects.R = c('9', 'clubs');
  var r = E.apply(s, { type: 'court', a: 'L', b: 'R' }); // S.R = 5 hearts pairs E.L = 5 clubs
  assert(r.state.lanes.cSE.paired);
  assert.strictEqual(r.state.lanes.cSE.gem, false, 'collected');
  assert.strictEqual(r.state.players.S.gems, before + 1, 'S controls cSE and collects');
  assert(r.events.some(function (e) { return e.type === 'collect' && e.seat === 'S'; }));
});

test('stalemated gem sits until control changes, then is collected', function () {
  var s = board({
    S: [c('2', 'hearts'), c('3', 'hearts'), c('9', 'clubs')],
    E: [c('5', 'clubs'), c('4', 'diamonds'), c('6', 'diamonds')],
    N: [c('7', 'hearts'), c('8', 'diamonds'), c('2', 'spades')],
    W: [c('3', 'clubs'), c('6', 'spades'), c('4', 'spades')]
  });
  s.courts.S.subjects.L = c('8', 'spades');
  var r = E.apply(s, { type: 'court', a: 'L', b: 'C' }); // S.C = 8 pairs N.C = 8 at the peak
  assert(r.state.lanes.pSN.paired);
  assert.strictEqual(r.state.lanes.pSN.gem, true, 'stalemate: gem stays');
  // Next: S moves its Jack to the centre; J beats K, S controls the peak.
  var s2 = r.state; s2.players.S.gems = 1;
  var r2 = E.apply(s2, { type: 'royal', a: 'L', b: 'C' });
  assert.strictEqual(E.controller(r2.state, 'pSN'), 'S');
  assert.strictEqual(r2.state.lanes.pSN.gem, false);
  assert(r2.events.some(function (e) { return e.type === 'collect' && e.lane === 'pSN' && e.seat === 'S'; }));
});

test('flush pays the court owner', function () {
  var s = board({
    S: [c('2', 'spades'), c('3', 'spades'), c('9', 'clubs')],
    E: [c('5', 'clubs'), c('4', 'diamonds'), c('6', 'diamonds')],
    N: [c('7', 'hearts'), c('8', 'diamonds'), c('2', 'clubs')],
    W: [c('3', 'clubs'), c('6', 'hearts'), c('4', 'hearts')]
  });
  s.players.S.hand = [c('9', 'spades')];
  var r = E.apply(s, { type: 'play', hand: 0, pos: 'R' });
  assert(r.events.some(function (e) { return e.type === 'flush' && e.seat === 'S'; }));
  assert.strictEqual(r.state.players.S.gems, 1);
  assert.strictEqual(r.state.deck[r.state.deck.length - 1].id, '9c', 'displaced card to the bottom of the deck');
});

test('all ten lanes paired ends the game; most gems wins', function () {
  var s = board({
    S: [c('3', 'spades'), c('5', 'hearts'), c('4', 'clubs')],
    E: [c('4', 'hearts'), c('5', 'clubs'), c('6', 'clubs')],
    N: [c('6', 'diamonds'), c('5', 'spades'), c('2', 'clubs')],
    W: [c('2', 'hearts'), c('A', 'diamonds'), c('7', 'diamonds')]
  });
  // Everything paired except cWS: W.R=7 vs S.L=3. Swap S.L into place via hand.
  s.players.S.hand = [c('7', 'clubs')];
  s.players.N.gems = 3;
  var r = E.apply(s, { type: 'play', hand: 0, pos: 'L' });
  assert.strictEqual(r.state.phase, 'over');
  assert.strictEqual(r.state.endReason, 'pyramid');
  var g = E.geometry(r.state);
  assert(g.complete && g.apexUnified && g.baseClosed);
  assert.strictEqual(g.faces.W.C, 5, 'ace at the apex takes the common value');
  // S closed it: the capstone (+5) lifts S past N.
  assert(r.events.some(function (e) { return e.type === 'capstone' && e.seat === 'S' && e.gems === 5; }));
  assert.deepStrictEqual(r.state.winners, ['S']);
  var r0 = E.apply(Object.assign(E.clone(s), { rules: Object.assign({}, s.rules, { capstone: 0 }) }), { type: 'play', hand: 0, pos: 'L' });
  assert.deepStrictEqual(r0.state.winners, ['N'], 'without the capstone N wins');
});

test('two aces paired make 1', function () {
  var s = board({
    S: [c('3', 'spades'), c('5', 'hearts'), c('A', 'clubs')],
    E: [c('A', 'hearts'), c('5', 'clubs'), c('6', 'clubs')],
    N: [c('6', 'diamonds'), c('5', 'spades'), c('2', 'clubs')],
    W: [c('2', 'hearts'), c('A', 'diamonds'), c('7', 'diamonds')]
  });
  assert.strictEqual(E.vertexValue(s, 'S', 'R'), 1);
  assert.strictEqual(E.vertexValue(s, 'E', 'L'), 1);
});

test('one gem per lane per turn: no farming', function () {
  var s = board({
    S: [c('5', 'hearts'), c('3', 'hearts'), c('9', 'clubs')],
    E: [c('5', 'clubs'), c('4', 'diamonds'), c('6', 'diamonds')],
    N: [c('7', 'hearts'), c('8', 'diamonds'), c('2', 'spades')],
    W: [c('3', 'clubs'), c('6', 'spades'), c('4', 'spades')]
  });
  s.players.S.gems = 10;
  var r = E.apply(s, { type: 'court', a: 'L', b: 'R' }); // pair
  var g1 = r.state.players.S.gems;
  r = E.apply(r.state, { type: 'court', a: 'L', b: 'R' }); // break
  r = E.apply(r.state, { type: 'court', a: 'L', b: 'R' }); // re-pair: no new gem
  assert.strictEqual(r.state.players.S.gems, g1 - 2);
});

test('clock: the game ends after maxRounds', function () {
  var s = E.newGame({ seed: 9, maxRounds: 2 });
  for (var i = 0; i < 8 && s.phase === 'play'; i++) s = E.apply(s, { type: 'pass' }).state;
  assert.strictEqual(s.phase, 'over');
  assert.strictEqual(s.endReason, 'clock');
});

test('AI games terminate and keep invariants', function () {
  var ends = { pyramid: 0, clock: 0 }, turns = 0;
  for (var g = 0; g < 16; g++) {
    var s = E.newGame({ seed: 'ai' + g });
    var rng = E.mulberry32(g + 7);
    var level = ['easy', 'normal', 'hard', 'master'][g % 4];
    var guard = 0, acted = 0, cur = s.current;
    while (s.phase === 'play' && guard++ < 5000) {
      if (s.current !== cur) { cur = s.current; acted = 0; }
      var a = AI.choose(s, { persona: AI.persona(E.SEATS.indexOf(s.current)), level: level, rng: rng, actionsThisTurn: acted });
      var r = E.apply(s, a);
      assert(!r.error, 'AI chose an illegal action: ' + JSON.stringify(a) + ' ' + r.error);
      s = r.state; acted++;
      // 52 distinct cards always.
      var ids = {};
      s.deck.forEach(function (x) { ids[x.id] = 1; });
      E.SEATS.forEach(function (seat) {
        E.POS.forEach(function (p) { ids[s.courts[seat].subjects[p].id] = 1; ids[s.courts[seat].royals[p].id] = 1; });
        s.players[seat].hand.forEach(function (x) { ids[x.id] = 1; });
        assert(s.players[seat].gems >= 0, 'negative gems');
      });
      assert.strictEqual(Object.keys(ids).length, 52);
    }
    assert(s.phase === 'over', 'game did not end');
    ends[s.endReason]++;
    turns += s.turn;
  }
  console.log('  16 AI games: ' + ends.pyramid + ' closed the pyramid, ' + ends.clock + ' ran out the clock; mean turns ' + (turns / 16).toFixed(1));
});

console.log(passed + ' passed' + (process.exitCode ? ', some FAILED' : ''));
