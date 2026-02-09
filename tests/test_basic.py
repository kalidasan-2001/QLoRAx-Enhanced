def test_dummy():
    assert True


def test_data_validation():
    from src.data_engineering.validate import validate_line

    valid, _ = validate_line(
        {
            "messages": [
                {"role": "user", "content": "Short"},
                {"role": "assistant", "content": "Also short"},
            ]
        },
        1,
    )
    assert not valid  # Should fail length check
