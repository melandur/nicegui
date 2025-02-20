from nicegui import ui

from ..documentation_tools import text_demo


def main_demo() -> None:
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
        {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]
    ui.table(columns=columns, rows=rows, row_key='name')


def more() -> None:
    @text_demo('Table with expandable rows', '''
        Scoped slots can be used to insert buttons that toggle the expand state of a table row.
        See the [Quasar documentation](https://quasar.dev/vue-components/table#expanding-rows) for more information.
    ''')
    def table_with_expandable_rows():
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'age', 'label': 'Age', 'field': 'age'},
        ]
        rows = [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol'},
        ]

        table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')
        table.add_slot('header', r'''
            <q-tr :props="props">
                <q-th auto-width />
                <q-th v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.label }}
                </q-th>
            </q-tr>
        ''')
        table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td auto-width>
                    <q-btn size="sm" color="accent" round dense
                        @click="props.expand = !props.expand"
                        :icon="props.expand ? 'remove' : 'add'" />
                </q-td>
                <q-td v-for="col in props.cols" :key="col.name" :props="props">
                    {{ col.value }}
                </q-td>
            </q-tr>
            <q-tr v-show="props.expand" :props="props">
                <q-td colspan="100%">
                    <div class="text-left">This is {{ props.row.name }}.</div>
                </q-td>
            </q-tr>
        ''')

    @text_demo('Show and hide columns', '''
        Here is an example of how to show and hide columns in a table.
    ''')
    def show_and_hide_columns():
        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
        ]
        rows = [
            {'name': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol'},
        ]
        visible_columns = {column['name'] for column in columns}
        table = ui.table(columns=columns, rows=rows, row_key='name')

        def toggle(column: dict, visible: bool) -> None:
            if visible:
                visible_columns.add(column['name'])
            else:
                visible_columns.remove(column['name'])
            table._props['columns'] = [column for column in columns if column['name'] in visible_columns]
            table.update()

        with ui.button(on_click=lambda: menu.open()).props('icon=menu'):
            with ui.menu() as menu, ui.column().classes('gap-0 p-2'):
                for column in columns:
                    ui.switch(column['label'], value=True, on_change=lambda e, column=column: toggle(column, e.value))

    @text_demo('Table with drop down selection', '''
        Here is an example of how to use a drop down selection in a table.
        After emitting a `rename` event from the scoped slot, the `rename` function updates the table rows.
    ''')
    def table_with_drop_down_selection():
        from typing import Dict

        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'age', 'label': 'Age', 'field': 'age'},
        ]
        rows = [
            {'id': 0, 'name': 'Alice', 'age': 18},
            {'id': 1, 'name': 'Bob', 'age': 21},
            {'id': 2, 'name': 'Carol'},
        ]
        name_options = ['Alice', 'Bob', 'Carol']

        def rename(msg: Dict) -> None:
            for row in rows:
                if row['id'] == msg['args']['id']:
                    row['name'] = msg['args']['name']
            ui.notify(f'Table.rows is now: {table.rows}')

        table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-full')
        table.add_slot('body', r'''
            <q-tr :props="props">
                <q-td key="name" :props="props">
                    <q-select
                        v-model="props.row.name"
                        :options="''' + str(name_options) + r'''"
                        @update:model-value="() => $parent.$emit('rename', props.row)"
                    />
                </q-td>
                <q-td key="age" :props="props">
                    {{ props.row.age }}
                </q-td>
            </q-tr>
        ''')
        table.on('rename', rename)

    @text_demo('Table from pandas dataframe', '''
        Here is a demo of how to create a table from a pandas dataframe.
    ''')
    def table_from_pandas_demo():
        import pandas as pd

        df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
        ui.table(
            columns=[{'name': col, 'label': col, 'field': col} for col in df.columns],
            rows=df.to_dict('records'),
        )
