from pathlib import Path


def test_memory_audit_uses_its_own_llm_timeout():
    source = Path("app.py").read_text()
    start = source.index("_TIMEOUT_EXEMPT_PREFIXES =")
    end = source.index("\n)\n", start)
    timeout_exemptions = source[start:end]

    assert '"/api/memory/audit"' in timeout_exemptions



def test_memory_audit_llm_call_uses_shared_stream_timeout():
    # A hard-coded 120s inactivity timeout was shorter than a local reasoning
    # model's prefill on a large memory list, so every Tidy attempt timed out.
    source = Path("services/memory/memory_extractor.py").read_text()
    audit = source[source.index("async def audit_memories("):]

    assert "timeout=LLMConfig.STREAM_TIMEOUT" in audit
    assert "timeout=120" not in audit
