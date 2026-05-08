import dns.resolver


def verify_txt_record(domain_name: str, expected_value: str) -> bool:
    """
    Check whether a TXT record exists at `domain_name` that exactly matches `expected_value`.
    """
    try:
        answers = dns.resolver.resolve(domain_name, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.decode('utf-8') == expected_value:
                    return True
        return False
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.NoNameservers,
        dns.exception.Timeout,
    ):
        return False