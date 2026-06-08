# Drill 9A — SPARQL on a Fixture KG

Complete `queries/drill.py` so each of `q1()` through `q5()` returns the SPARQL query the matching docstring describes. The autograder parses `fixtures/mini_kg.ttl` with `rdflib`, runs each query, and checks the result set.

Run locally:

```bash
pip install -r requirements.txt
pytest tests/ -v
```

No Docker or Fuseki needed — everything runs in-memory against `rdflib`.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
