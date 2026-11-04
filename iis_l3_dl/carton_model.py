#!/usr/bin/env python3
"""The carton RWMS of Lectures 3a and 3b as a small closed-loop dynamical system.

BWS_theta = <S, A, O, D, T_theta, Omega_theta, S0>  (body-world system, indexed by theta)
ME        = <Z, z0, g, kappa>                       (executive with internal state)
One interaction round: o_k in Omega(s_k); a_k = kappa(z_k, o_k); z_{k+1} = g(z_k, o_k);
s_{k+1} in T(s_k, a_k, d_k).

The model is event-level: one round per action token, and a token spans an interval
whose duration is declared (A4).  All numbers are teaching assumptions A1-A6:
  A1  Coulomb two-finger pinch holds at vertical acceleration a iff 2*mu*F >= m*(g + a).
  A2  A pinch that slips within a 5 mm test lift lets the carton settle upright, and the slip
      leaves the pinch shifted: carrying on from it without a new grasp tips the open carton and
      spills it. A slipping pinch that keeps rising also tips and spills the carton.
  A3  A palm-under grasp carries any carton in the family at 0.5 m/s^2.
  A4  Durations: test lift 2 s, pinch carry 12 s, palm-under placement 12 s,
      palm carry 12 s, decline 3 s.
  A5  Squeezing above 25 N dents the carton.
  A6  The camera cannot see wetness; K_blind has no slip or load sensing.
"""
from dataclasses import dataclass, field

G = 9.81
DENT = 25.0


def holds(mu, m, force, accel):
    """A1: does a two-finger pinch with this force hold at this vertical acceleration?"""
    return 2 * mu * force >= m * (G + accel) - 1e-12


@dataclass
class Theta:
    """Index of one BWS in the family: body parameters and world parameters."""
    body: str          # 'K_tac' or 'K_blind'
    mu: float          # world: friction
    m: float           # world: mass in kg


@dataclass
class State:
    mode: str = 'on shelf'      # on shelf, pinched, lifted, settled, slipping, tipped, on palm, at mug, declined
    height_mm: float = 0
    force: float = 0
    spill: bool = False
    dent: bool = False
    t: float = 0

    def show(self):
        flags = (' · spill' if self.spill else '') + (' · dent' if self.dent else '')
        return f'{self.mode}{flags}'


def observe(theta, s, last_token):
    """Omega_theta: what the executive receives. K_blind has a camera only."""
    if theta.body == 'K_blind':
        return {'slip': '—', 'load': '—', 'camera': 'carton' if s.mode != 'at mug' else 'at mug'}
    slip = s.mode in ('settled', 'slipping') and last_token.startswith('lift')
    load = round(theta.m, 2) if s.mode in ('lifted', 'on palm', 'at mug') else 0.0
    return {'slip': 'yes' if slip else 'no', 'load': load,
            'camera': 'at mug' if s.mode == 'at mug' else 'carton'}


def transition(theta, s, token):
    """T_theta, written as modes with guards (a hybrid automaton at event level)."""
    n = State(**vars(s))
    if token == 'pinch 18 N':
        n.mode, n.force, n.t = 'pinched', 18, s.t
        n.dent = 18 > DENT
    elif token == 'lift 5 mm, 1 m/s²':
        n.t = s.t + 2
        if holds(theta.mu, theta.m, s.force, 1.0):
            n.mode, n.height_mm = 'lifted', 5
        else:
            n.mode, n.height_mm = 'settled', 0          # A2: slip within 5 mm settles upright
    elif token in ('carry 0.5 m/s²', 'lift and carry 1 m/s²'):
        accel = 0.5 if token.startswith('carry') else 1.0
        n.t = s.t + 12
        if s.mode == 'lifted' or (s.mode == 'pinched' and holds(theta.mu, theta.m, s.force, accel)):
            n.mode = 'at mug'
        else:                                           # A2: slipping pinch keeps rising
            n.mode, n.spill = 'tipped', True
    elif token == 'palm-under':
        n.mode, n.force, n.t = 'on palm', 0, s.t + 12
    elif token == 'carry on palm 0.5 m/s²':
        n.mode, n.t = 'at mug', s.t + 12                # A3
    elif token == 'decline':
        n.mode, n.t = 'declined', s.t + 3
    return n


# ---------------------------------------------------------------- executives
# Each executive is <Z, z0, g, kappa>; kappa returns the token, g the next internal state.
def E_B(z, o):
    """Test, then commit: kappa and g in one table."""
    if z == 'start':
        return 'pinch 18 N', 'grasped'
    if z == 'grasped':
        return 'lift 5 mm, 1 m/s²', 'testing'
    if z == 'testing':
        return ('palm-under', 'fallback') if o['slip'] == 'yes' else ('carry 0.5 m/s²', 'done')
    if z == 'fallback':
        return 'carry on palm 0.5 m/s²', 'done'
    return 'stop', 'done'


def E_A(z, o):
    if z == 'start':
        return 'pinch 18 N', 'grasped'
    if z == 'grasped':
        return 'lift and carry 1 m/s²', 'done'
    return 'stop', 'done'


EXECUTIVES = {'E_A': E_A, 'E_B': E_B}


def execute(executive, theta, max_rounds=8):
    """One maximal execution of the closed loop; returns rounds (k, s_k, o_k, z_k, a_k)."""
    policy = EXECUTIVES[executive]
    s, z, last, rounds = State(), 'start', '', []
    for k in range(max_rounds):
        o = observe(theta, s, last)
        a, z_next = policy(z, o)
        rounds.append({'k': k, 't': s.t, 's': s.show(), 'o': o, 'z': z, 'a': a})
        if a == 'stop':
            break
        s, z, last = transition(theta, s, a), z_next, a
    return rounds


def fmt_obs(o):
    return f"slip {o['slip']} · load {o['load']} · cam {o['camera']}"


if __name__ == '__main__':
    for body in ('K_tac', 'K_blind'):
        for mu in (0.55, 0.19):
            print(f'\nE_B on {body}, mu={mu}, m=0.64')
            for r in execute('E_B', Theta(body, mu, 0.64)):
                print(f"  k={r['k']} t={r['t']:>4} s={r['s']:<18} o=({fmt_obs(r['o'])}) z={r['z']:<9} a={r['a']}")
