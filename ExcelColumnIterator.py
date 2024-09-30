class ExcelColumnIterator:
    def __init__(self):
        self.column_name = ''

    def __iter__(self):
        return self

    def __next__(self):
        if not self.column_name:
            self.column_name = 'A'
            return self.column_name

        # Increment column name
        columns = list(self.column_name)
        for i in range(len(columns) - 1, -1, -1):
            if columns[i] == 'Z':
                columns[i] = 'A'
            else:
                columns[i] = chr(ord(columns[i]) + 1)
                break
        else:
            columns.insert(0, 'A')

        self.column_name = ''.join(columns)
        return self.column_name

# Usage
column_iterator = ExcelColumnIterator()

for _ in range(100):
    print(next(column_iterator))
