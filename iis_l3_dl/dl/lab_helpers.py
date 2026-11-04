"""Small helpers for the Sheet 3 description-logic lab (Task 8). Each call builds a fresh copy of the course's
teaching ontology, so experiments do not leak into each other."""
import types

from owlready2 import World, OneOf, Thing, sync_reasoner, OwlReadyInconsistentOntologyError

import rwms_ontology as R


def fresh(extend=None):
    """A new world with the teaching ontology; `extend(o, D)` may add classes, axioms and individuals.
    o is the course ontology (o.Carton, o["pr2_body"], ...), D the DUL namespace (D.PhysicalArtifact, D.hasComponent, ...)."""
    w = World()
    o = R.build(w)
    D = o.get_namespace(R.DUL_IRI)
    if extend:
        with o:
            extend(o, D)
    return o, D


def consistent(extend=None):
    """True if the ontology (with your extension) is consistent according to HermiT."""
    o, D = fresh(extend)
    try:
        with o:
            sync_reasoner(o.world, infer_property_values=False, debug=0)
        return True
    except OwlReadyInconsistentOntologyError:
        return False


def wholes_of(part, candidates, extend=None):
    """The individuals among `candidates` of which `part` is a part, as classified by HermiT (via PartOf_x ≡ ∃isPartOf.{x})."""
    o, D = fresh(extend)
    with o:
        for n in candidates:
            q = types.new_class("PartOf_" + n, (Thing,))
            q.equivalent_to.append(D.isPartOf.some(OneOf([o[n]])))
        sync_reasoner(o.world, infer_property_values=False, debug=0)
    return [n for n in candidates if o["PartOf_" + n] in o[part].INDIRECT_is_a]
