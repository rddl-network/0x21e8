from x21e8.models.issuing_request import IssuingRequest
from x21e8.routers.machine import check_if_tokens_should_be_issued


def test_both_ticker_and_amount_not_set():
    input1 = IssuingRequest(
        name="XYZ",
        ticker="",
        amount=0,
        precision=0,
        public_url="https://test.org",
        reissue=False,
        cid="test",
    )
    expected_output1 = False
    assert check_if_tokens_should_be_issued(input1) == expected_output1


def test_ticker_set_but_amount_is_0():
    input2 = IssuingRequest(
        name="XYZ",
        ticker="XYZ",
        amount=0,
        precision=0,
        public_url="https://test.org",
        reissue=False,
        cid="test",
    )
    expected_output2 = True
    assert check_if_tokens_should_be_issued(input2) == expected_output2


def test_ticker_not_set_and_amount_set():
    input3 = IssuingRequest(
        name="XYZ",
        ticker="",
        amount=100,
        precision=0,
        public_url="https://test.org",
        reissue=False,
        cid="test",
    )
    expected_output3 = True
    assert check_if_tokens_should_be_issued(input3) == expected_output3


def test_both_ticker_and_amount_set():
    input3 = IssuingRequest(
        name="XYZ",
        ticker="XYZ",
        amount=100,
        precision=0,
        public_url="https://test.org",
        reissue=False,
        cid="test",
    )
    expected_output3 = True
    assert check_if_tokens_should_be_issued(input3) == expected_output3
