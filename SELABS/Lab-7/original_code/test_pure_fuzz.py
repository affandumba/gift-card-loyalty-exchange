from hypothesis import given, strategies as st
from tennis_scoring import parse_score, game_lead, set_spread

@given(st.text() | st.none())
def test_parse_score_no_crash(s):
    try:
        parse_score(s)
    except Exception as e:
        assert False, f"parse_score crashed with: {e!r} on input {s!r}"
