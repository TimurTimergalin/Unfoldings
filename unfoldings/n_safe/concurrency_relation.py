from alg import Co


# Отличие от базового Co в том, что 2 условия, помеченные одинаковой позицией,
# в co-set-е присутствовать не должны
class NSafeCo(Co):
    def create_new_allowed(self, allowed, current, el, n, sorted_co):
        new_allowed = set()
        while current < n and (pair := sorted_co[current])[0] == el:
            if pair[1].place != el.place:
                new_allowed.add(pair[1])
            current += 1

        if allowed is not None:
            new_allowed &= allowed
        return current, new_allowed
