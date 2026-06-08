"""Autograder for Drill 9A — SPARQL on a fixture KG."""

import os
import sys

import pytest
from rdflib import Graph, URIRef

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from queries.drill import q1, q2, q3, q4, q5  # noqa: E402

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "fixtures", "mini_kg.ttl")
NS = "http://example.org/library/"


@pytest.fixture(scope="module")
def g():
    graph = Graph()
    graph.parse(FIXTURE, format="turtle")
    return graph


def test_q1_all_books(g):
    sparql = q1()
    assert sparql.strip(), "q1() returned an empty string."
    rows = list(g.query(sparql))
    assert len(rows) == 5, f"q1 expected 5 rows; got {len(rows)}."
    assert all(len(r) == 2 for r in rows), "q1 must SELECT ?book ?title."


def test_q2_post_2010(g):
    sparql = q2()
    assert sparql.strip(), "q2() returned an empty string."
    rows = list(g.query(sparql))
    assert len(rows) == 1, (
        f"q2 expected 1 row (the post-2010 book); got {len(rows)}. "
        f"Use FILTER (?year > 2010) — strict, not >=."
    )


def test_q3_book_author_name(g):
    sparql = q3()
    assert sparql.strip(), "q3() returned an empty string."
    rows = list(g.query(sparql))
    assert len(rows) == 7, (
        f"q3 expected 7 rows (5 books, 2 books have 2 authors); got {len(rows)}. "
        f"Did you join through the author URI to rdfs:label?"
    )


def test_q4_optional_topic(g):
    sparql = q4()
    assert sparql.strip(), "q4() returned an empty string."
    rows = list(g.query(sparql))
    assert len(rows) == 5, (
        f"q4 expected 5 rows (every book appears); got {len(rows)}. "
        f"Books without :topic must still appear via OPTIONAL."
    )
    unbound = [r for r in rows if r[1] is None]
    assert unbound, (
        "q4 expected ≥1 row with unbound ?topic. If every row has a topic, "
        "you used WHERE instead of OPTIONAL — papers without topic dropped."
    )


def test_q5_ask_multiple_authors(g):
    sparql = q5()
    assert sparql.strip(), "q5() returned an empty string."
    # Verdict check: must return True on the real fixture.
    assert bool(g.query(sparql)) is True, (
        "q5 should return True — book1 and book5 each have multiple authors."
    )
    # Shape check: a wildcard ASK { ?x ?y ?z } also returns True on a non-empty
    # graph, so we additionally require the query to mention :author and to
    # bind two distinct authors. Without this, the test silently passes any
    # ASK against the fixture.
    text = sparql
    assert ":author" in text, (
        "q5 must constrain on :author — a wildcard ASK passes on any non-empty graph."
    )
    # On a degraded single-author graph the answer should be False.
    g_single = Graph()
    g_single.parse(
        data="""@prefix : <http://example.org/library/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        :soloAuthor rdfs:label "Solo Author" .
        :soloBook a :Book ; :title "Alone" ; :author :soloAuthor ; :year 2000 .
        """,
        format="turtle",
    )
    assert bool(g_single.query(sparql)) is False, (
        "q5 returned True on a single-author graph — the query did not actually "
        "test for multiple distinct authors on the same book."
    )
