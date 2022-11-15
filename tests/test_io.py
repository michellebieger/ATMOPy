"""Test IO functions."""


def test_namelist():
    """Test namelist generation."""
    from atmopy.io import create_namelist

    expected = """
&TEST
param1 = 12.4
param2 = 27
param3 = 'hello there'
    """

    test_value = create_namelist(
        "test",
        {
            "param1": 12.4,
            "param2": 27,
            "param3": "hello",
        },
    )

    assert test_value == expected
