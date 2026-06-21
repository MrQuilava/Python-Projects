from project import validate_email_format, classify_domain, check_suspicious_patterns

def test_validate_email_format():
    # Test BatStateU specific custom formats
    assert validate_email_format("22-12345@g.batstate-u.edu.ph") == "BSU"
    assert validate_email_format("25-99999@g.batstate-u.edu.ph") == "BSU"

    # Test typical valid layouts
    assert validate_email_format("testuser@gmail.com") == "GENERAL"
    assert validate_email_format("dan@gov") == "GENERAL"

    # Test completely broken formats
    assert validate_email_format("plainaddress") == "INVALID"
    assert validate_email_format("@missingusername.com") == "INVALID"


def test_classify_domain():
    assert classify_domain("gmail.com") == "Personal Account"
    assert classify_domain("edu.ph") == "PH Education"
    assert classify_domain("gov") == "Government Account"
    assert classify_domain("unknown-domain.xyz") == "Entity"
    # Verify case-insensitivity
    assert classify_domain("GMAIL.COM") == "Personal Account"


def test_check_suspicious_patterns():
    # Test heavy numeric loads (Bot signs)
    assert check_suspicious_patterns("botuser123456") is True
    assert check_suspicious_patterns("987654321") is True

    # Test high consonant string density (Gibberish strings)
    assert check_suspicious_patterns("bcdfghjk") is True
    assert check_suspicious_patterns("zxcvbnm") is True

    # Test clean accounts
    assert check_suspicious_patterns("dan_gabriel") is False
    assert check_suspicious_patterns("kels123") is False
    assert check_suspicious_patterns("calix") is False
