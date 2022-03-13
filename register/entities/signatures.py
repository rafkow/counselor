from ..models import Case
from re import search
from datetime import date


def __get_max_signature(signatures):
    if not signatures:
        return 1
    pattern = r'(?<=/)\w+'
    m = [search(pattern, x).group(0) for x in signatures if search(pattern, x)]
    m = [int(x) for x in m if x.isdigit()]
    m = max(m)
    return m+1


def next_signature():
    year = date.today().strftime('%y')
    m = Case.objects.filter(signature__regex=rf'M/\d+/{year}').values_list('signature', flat=True)
    k = Case.objects.filter(signature__regex=fr'K/\d+/{year}').values_list('signature', flat=True)
    result = [f'M/{__get_max_signature(m)}/{year}', f'K/{__get_max_signature(k)}/{year}']
    return result


