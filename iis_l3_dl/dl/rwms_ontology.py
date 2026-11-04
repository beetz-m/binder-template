#!/usr/bin/env python3
"""Lecture 3, DL variant: a small teaching ontology of the RWMS top level, and its competency questions.

The names follow the AICOR L2 ontology (foundation/okf/aicor/L2-conceptual-framework/ontology: core-classes,
robot-world-manipulation-system, body-world-system, manipulation-executive, robot-body, sensor, semantic-digital-twin,
designator, bws-relative-task-specification). The module is simplified for teaching and self-contained; it is not
the AICOR ontology. Every competency-question answer below is computed by a reasoner (HermiT; the numeric query by the causal
model of carton_model.py), never typed by hand. Run with owlready2 on the path, e.g.

    PYTHONPATH=~/.local/lib/python3.10/site-packages python3 dl/rwms_ontology.py

Writes rwms-teaching.owl and cq-results.json next to this file.
"""
import json
import types
from pathlib import Path

from owlready2 import (AllDisjoint, DataProperty, FunctionalProperty, ObjectProperty, Thing, TransitiveProperty,
                       default_world, get_ontology, Inverse, sync_reasoner,
                       OwlReadyInconsistentOntologyError)

HERE = Path(__file__).resolve().parent
IRI = "http://aicor.org/teaching/rwms-l3.owl#"


DUL_FILE = HERE / "DUL.owl"     # local copy of DUL (EASE copy, v3.34), so the lab runs anywhere
DUL_IRI = "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#"


def build(world=None):
    """Every concept specializes a DUL class (DOLCE+DnS Ultralite, the EASE copy, v3.34)."""
    from owlready2 import World, AllDifferent
    world = world or default_world
    dul_onto = world.get_ontology(DUL_FILE.as_uri()).load()
    D = dul_onto.get_namespace(DUL_IRI)
    onto = world.get_ontology(IRI)
    onto.imported_ontologies.append(dul_onto)
    with onto:
        # ------------------------------------------------------------ roles: DUL where it fits, our own otherwise
        hasPart, isPartOf = D.hasPart, D.isPartOf                # transitive, reflexive
        hasComponent, isComponentOf = D.hasComponent, D.isComponentOf   # simple: may carry number restrictions
        hasProperPart = D.hasProperPart
        isAbout = D.isAbout                                      # InformationObject -> Entity
        class controls(ObjectProperty): pass                     # executive -> body-world system
        class actsOn(ObjectProperty): pass                       # who receives the action tokens
        class observes(ObjectProperty): pass                     # executive -> observation
        class producedBy(ObjectProperty): pass                   # observation -> sensor
        class generates(ObjectProperty): pass                    # BWS -> trajectory
        class assessesTrajectory(ObjectProperty): pass           # problem -> trajectory (dul:classifies is taken)
        class assessedAgainst(ObjectProperty): pass              # RWMS -> problem
        class uses(ObjectProperty): pass                         # executive -> twin / designator
        class hasGoal(ObjectProperty): pass                      # designator / problem -> goal
        class activeDuring(ObjectProperty): pass                 # goal -> time interval

        # ------------------------------------------------------------ attributes (data properties)
        class mass(DataProperty, FunctionalProperty): range = [float]
        class frictionCoefficient(DataProperty, FunctionalProperty): range = [float]
        class gripForce(DataProperty, FunctionalProperty): range = [float]
        class liftAcceleration(DataProperty, FunctionalProperty): range = [float]
        class pinchHolds(DataProperty, FunctionalProperty): range = [bool]

        # ------------------------------------------------------------ concepts, each under a DUL class
        # not dul:PhysicalObject: DUL has PhysicalObject ⊑ ∀hasPart.PhysicalObject, and the executive is not physical
        class RobotWorldManipulationSystem(D.Object): pass
        class BodyWorldSystem(D.PhysicalObject): pass
        class RobotBody(D.PhysicalArtifact): pass
        class Link(D.PhysicalArtifact): pass
        class Joint(D.PhysicalArtifact): pass
        class Motor(D.PhysicalArtifact): pass
        class Sensor(D.PhysicalArtifact): pass
        class Camera(Sensor): pass
        class EndEffector(Link): pass
        class WorldEntity(D.PhysicalObject): pass
        class Container(WorldEntity): pass
        class Fridge(Container): pass
        class TransportableObject(WorldEntity): pass
        class Carton(TransportableObject): pass
        class Person(WorldEntity, D.NaturalPerson): pass
        class ManipulationExecutive(D.Agent): pass
        class BodyWorldTrajectory(D.Process): pass
        class Pinch(D.Action): pass
        class Observation(D.InformationObject): pass
        class ActionToken(D.InformationObject): pass
        class SemanticDigitalTwin(D.InformationObject): pass
        class Belief(D.InformationObject): pass
        class CausalModel(D.Theory): pass
        class ActionDesignator(D.Description): pass
        class Goal(D.Goal): pass
        class LifetimeGoal(Goal): pass
        class ManipulationProblem(D.Description): pass
        class AgentLifetime(D.TimeInterval): pass
        AllDisjoint([WorldEntity, RobotBody, BodyWorldSystem, RobotWorldManipulationSystem, Link, Joint, Motor, Sensor])
        AllDisjoint([Observation, ActionToken, SemanticDigitalTwin, Belief])
        AllDisjoint([ActionDesignator, Goal, ManipulationProblem, CausalModel])
        AllDisjoint([ManipulationExecutive, D.Description, D.PhysicalObject])

        # domains and ranges
        controls.domain = [ManipulationExecutive]; controls.range = [BodyWorldSystem]
        actsOn.domain = [ManipulationExecutive]; actsOn.range = [BodyWorldSystem]
        observes.domain = [ManipulationExecutive]; observes.range = [Observation]
        producedBy.domain = [Observation]; producedBy.range = [Sensor]
        generates.domain = [BodyWorldSystem]; generates.range = [BodyWorldTrajectory]
        assessesTrajectory.domain = [ManipulationProblem]; assessesTrajectory.range = [BodyWorldTrajectory]
        assessedAgainst.domain = [RobotWorldManipulationSystem]; assessedAgainst.range = [ManipulationProblem]
        hasGoal.range = [Goal]
        activeDuring.domain = [Goal]; activeDuring.range = [D.TimeInterval]

        # ------------------------------------------------------------ partonomy
        RobotWorldManipulationSystem.equivalent_to.append(
            hasComponent.exactly(1, ManipulationExecutive) & hasComponent.exactly(1, BodyWorldSystem))
        RobotWorldManipulationSystem.is_a.append(hasComponent.only(ManipulationExecutive | D.PhysicalObject))
        BodyWorldSystem.is_a += [hasComponent.exactly(1, RobotBody), hasComponent.some(WorldEntity),
                                 hasComponent.only(D.PhysicalObject), generates.some(BodyWorldTrajectory)]
        RobotBody.is_a += [hasComponent.some(Link), hasComponent.some(Joint), hasComponent.some(Sensor),
                           hasComponent.some(EndEffector)]
        Sensor.is_a.append(isPartOf.some(RobotBody))

        # ------------------------------------------------------------ axioms relating the concepts
        ManipulationExecutive.is_a += [hasProperPart.only(D.SocialObject),
                                       controls.some(BodyWorldSystem), actsOn.only(BodyWorldSystem),
                                       observes.only(Observation), uses.some(SemanticDigitalTwin),
                                       uses.some(ActionDesignator)]
        Observation.is_a.append(producedBy.some(Sensor))
        RobotWorldManipulationSystem.is_a.append(assessedAgainst.some(ManipulationProblem))
        ManipulationProblem.is_a += [assessesTrajectory.some(BodyWorldTrajectory), hasGoal.some(Goal)]
        SemanticDigitalTwin.is_a += [isAbout.some(BodyWorldSystem), hasComponent.some(Belief),
                                     hasComponent.some(CausalModel)]
        ActionDesignator.is_a.append(hasGoal.some(Goal))
        Goal.is_a.append(activeDuring.exactly(1, D.TimeInterval))
        LifetimeGoal.is_a.append(activeDuring.some(AgentLifetime))
        Carton.is_a += [mass.exactly(1, float), frictionCoefficient.exactly(1, float)]

        # ------------------------------------------------------------ individuals: the PR2 serves Eva a drink
        pr2_rwms = RobotWorldManipulationSystem("pr2_rwms")
        executive = ManipulationExecutive("pr2_executive")
        bws = BodyWorldSystem("pr2_apartment_bws")
        body = RobotBody("pr2_body")
        head_camera = Camera("pr2_head_camera")
        gripper = EndEffector("pr2_right_gripper")
        shoulder = Joint("pr2_r_shoulder_pan_joint")
        fridge = Fridge("apartment_fridge")
        carton = Carton("milk_carton", mass=0.64, frictionCoefficient=0.19)
        eva = Person("eva")
        twin = SemanticDigitalTwin("pr2_twin")
        belief = Belief("belief_carton_wet"); law = CausalModel("coulomb_pinch_law")
        ad = ActionDesignator("transport_carton_ad")
        goal = Goal("carton_at_mug_upright")
        safety = LifetimeGoal("no_harm_to_people")
        interval = D.TimeInterval("transport_interval"); life = AgentLifetime("pr2_lifetime")
        problem = ManipulationProblem("serve_drink_to_eva")
        obs = Observation("image_0042")
        pr2_rwms.hasComponent = [executive, bws]
        bws.hasComponent = [body, fridge, carton, eva]
        body.hasComponent = [head_camera, gripper, shoulder]
        executive.controls = [bws]; executive.actsOn = [bws]; executive.observes = [obs]; executive.uses = [twin, ad]
        obs.producedBy = [head_camera]
        twin.isAbout = [bws]; twin.hasComponent = [belief, law]
        ad.hasGoal = [goal]; goal.activeDuring = [interval]; safety.activeDuring = [life]
        pr2_rwms.assessedAgainst = [problem]; problem.hasGoal = [goal]
        # a second system given only by its parts: will the reasoner recognise it as an RWMS?
        tiago_exec = ManipulationExecutive("tiago_executive"); tiago_bws = BodyWorldSystem("tiago_kitchen_bws")
        tiago_system = D.Object("tiago_system"); tiago_system.hasComponent = [tiago_exec, tiago_bws]
        AllDifferent([i for i in onto.individuals() if i.namespace == onto])
        tiago_system.is_a.append(hasComponent.only(OneOfSelf(onto, [tiago_exec, tiago_bws])))
    return onto


def OneOfSelf(onto, inds):
    from owlready2 import OneOf
    return OneOf(inds)


def reason(onto):
    with onto:
        sync_reasoner(onto.world if hasattr(onto, "world") else default_world, infer_property_values=True, debug=0)


def run():
    results = []
    onto = build()
    from owlready2 import types as _t, OneOf
    D = onto.get_namespace(DUL_IRI)
    candidates = ["pr2_body", "pr2_apartment_bws", "pr2_rwms", "pr2_executive", "pr2_twin"]
    with onto:                       # query classes: PartOf_x ≡ ∃isPartOf.{x}, classified by the reasoner
        for n in candidates:
            q = _t.new_class("PartOf_" + n, (Thing,))
            q.equivalent_to.append(D.isPartOf.some(OneOf([onto[n]])))
    reason(onto)
    O = lambda n: onto[n]

    def parts_closure(ind):
        return sorted(i.name for i in ind.INDIRECT_partOf) if hasattr(ind, "INDIRECT_partOf") else []

    # CQ1 partonomy: of which wholes is the head camera a part?
    inds = set(onto.individuals())
    cam = O("pr2_head_camera")
    wholes = sorted(n for n in candidates if onto["PartOf_" + n] in cam.INDIRECT_is_a)   # classified by HermiT
    results.append({"id": "CQ1", "question": "Of which wholes is the PR2's head camera a part?",
                    "answer": wholes, "how": "dul:isPartOf is transitive; dul:hasComponent ⊑ dul:hasProperPart ⊑ dul:hasPart",
                    "uses": ["partonomy", "transitive role"]})
    # CQ2 recognition: is tiago_system an RWMS?
    is_rwms = O("RobotWorldManipulationSystem") in O("tiago_system").INDIRECT_is_a
    results.append({"id": "CQ2", "question": "A system has exactly one executive and one body–world system as parts. Is it an RWMS?",
                    "answer": is_rwms, "how": "the definition RWMS ≡ (=1 hasComponent.ME) ⊓ (=1 hasComponent.BWS) classifies it",
                    "uses": ["equivalence axiom", "number restriction"]})
    # CQ3 inferred types from roles
    inferred = sorted(c.name for c in O("image_0042").is_a if getattr(c, "namespace", None) == onto)
    results.append({"id": "CQ3", "question": "What does the reasoner know about image_0042, given only that the executive observes it?",
                    "answer": inferred, "how": "range of observes, axiom Observation ⊑ ∃producedBy.Sensor",
                    "uses": ["range axiom"]})
    # CQ4 the problem is not a part; CQ5 the executive cannot act on the carton directly; CQ6 an executive is not a body part
    for qid, question, mutate, uses in [
        ("CQ4", "Can the manipulation problem be a part of the RWMS?",
         lambda o: o["pr2_rwms"].hasComponent.append(o["serve_drink_to_eva"]), ["value restriction ∀hasComponent", "disjointness"]),
        ("CQ5", "Can the executive act on the milk carton directly?",
         lambda o: o["pr2_executive"].actsOn.append(o["milk_carton"]), ["value restriction ∀actsOn", "disjointness"]),
        ("CQ9", "Can the RWMS be a dul:PhysicalObject, as a robot plus its world might suggest?",
         lambda o: o["RobotWorldManipulationSystem"].is_a.append(o.get_namespace(DUL_IRI).PhysicalObject),
         ["DUL: PhysicalObject ⊑ ∀hasPart.PhysicalObject", "executive is a non-physical dul:Agent"]),
        ("CQ6", "Can the head camera be a part of the executive?",
         lambda o: o["pr2_executive"].hasComponent.append(o["pr2_head_camera"]), ["value restriction ∀hasProperPart.dul:SocialObject", "DUL disjointness"]),
    ]:
        w = types.SimpleNamespace()
        from owlready2 import World
        world = World()
        o = build(world)
        with o:
            mutate(o)
        try:
            with o:
                sync_reasoner(world, infer_property_values=False, debug=0)
            consistent = True
        except OwlReadyInconsistentOntologyError:
            consistent = False
        results.append({"id": qid, "question": question, "answer": "no" if not consistent else "yes (consistent)",
                        "how": "adding the statement makes the ontology inconsistent" if not consistent else "consistent",
                        "uses": uses})
    # CQ7 goal intervals
    g = O("carton_at_mug_upright").activeDuring; s = O("no_harm_to_people").activeDuring
    results.append({"id": "CQ7", "question": "While which interval must each goal hold?",
                    "answer": {"carton_at_mug_upright": [x.name for x in g], "no_harm_to_people": [x.name for x in s]},
                    "how": "activeDuring; LifetimeGoal ⊑ ∃activeDuring.AgentLifetime (⊑ dul:TimeInterval)", "uses": ["role", "subclass"]})
    # CQ8 the limit of DL: does the 18 N pinch hold the wet carton in the 1 m/s² test lift?
    results.append(cq_rule())
    onto.save(file=str(HERE / "rwms-teaching.owl"), format="rdfxml")
    (HERE / "cq-results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
    for r in results:
        print(r["id"], r["answer"])
    return results


def cq_rule():
    """DL has no arithmetic: the TBox cannot entail whether a pinch holds. The twin's causal model can."""
    import sys
    from owlready2 import World
    world = World()
    o = build(world)
    with o:
        p = o.Pinch("test_lift_pinch", gripForce=18.0, liftAcceleration=1.0, frictionCoefficient=0.19, mass=0.64)
        sync_reasoner(world, infer_property_values=True, debug=0)       # HermiT: description logic only
    dl_answer = p.pinchHolds
    sys.path.insert(0, str(HERE.parent))
    import carton_model as cm                                          # the causal model, axiom A1
    holds = cm.holds(0.19, 0.64, 18.0, 1.0)
    return {"id": "CQ8", "question": "Does the 18 N pinch hold the wet carton (μ = 0.19, 0.64 kg) in the 1 m/s² test lift?",
            "answer": {"description logic (HermiT)": "no answer" if dl_answer is None else dl_answer,
                       "causal model A1 in the twin (carton_model.py)": "holds" if holds else "slips"},
            "how": "DL has no arithmetic; the Coulomb law A1 lives in the twin's causal model",
            "uses": ["limit of DL", "causal model"]}


if __name__ == "__main__":
    run()
