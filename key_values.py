class KeyValues:
    @staticmethod
    def parse(data):
        cur = 0
        end = len(data)
        parsed = KeyValues.parse_properties(data, cur, end)
        return parsed[0]

    @staticmethod
    def parse_properties(data, cur, end):
        pairs = {}
        entity = None

        parsing_key = True
        key = None

        while cur < end:
            if data[cur].isspace():
                pass
            elif data[cur] == '"':
                if entity is None:
                    # Opening quote, prepare a buffer for the entity
                    entity = []
                else:
                    # Closing quote, store the parsed entity
                    entity = ''.join(entity)
                    if parsing_key:
                        key = entity
                    else:
                        pairs[key] = entity
                    # Keys and values always alternate
                    parsing_key = not parsing_key
                    entity = None
            elif data[cur] == '{':
                # The current key is a parent.
                pairs[key], cur  = KeyValues.parse_properties(data, cur + 1, end)
                parsing_key = True
            elif data[cur] == '}':
                # We're done parsing for the parent's key
                return (pairs, cur + 1)
            else:
                entity.append(data[cur])
            cur += 1

        return (pairs, cur)
