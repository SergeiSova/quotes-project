import hashlib
from math import sqrt


def make_fingerprint(request) -> str:
    """Собираем стабильный отпечаток для антидублей голосов.
    Приватности ради — хешируем.
    """
    if not request.session.session_key:
        request.session.save()
    sess = request.session.session_key or ''
    ip = (request.META.get('REMOTE_ADDR') or '')[:45]
    ua = (request.META.get('HTTP_USER_AGENT') or '')[:120]
    raw = f'{sess}|{ip}|{ua}'.encode('utf-8', 'ignore')
    return hashlib.sha256(raw).hexdigest()


def wilson_lower_bound(up: int, down: int, confidence: float = 0.95) -> float:
    n = up + down
    if n == 0:
        return 0.0
    from math import erf, sqrt

    z = 1.959963984540054  
    phat = up / n
    denom = 1 + z*z/n
    num = phat + z*z/(2*n) - z*sqrt((phat*(1-phat) + z*z/(4*n))/n)
    return num / denom
