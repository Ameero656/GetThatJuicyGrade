import PySimpleGUI as sg
import pyperclip
import json
from json import JSONDecodeError
import re


DECIMAL_PATTERN = r'(\d+(?:\.\d*)?)'

 
assignments ={}

sg.theme('DarkAmber')
summative_scale, formative_scale = 0, 0


sf_scale_layout = [
    
    [sg.Text('Summative Scale:'),sg.InputText(size=3, key='summative_scale')],
    [sg.Text('Formative Scale:'),sg.InputText(size=3, key='formative_scale')],
    [sg.Button('Update Scale')]
    
    ]

formative_assignments_layout = [
    [sg.Listbox(values=({}), size=(30, 5), key='formative_assignments')],

]

summative_assignments_layout = [[sg.Listbox(values=({}), size=(30, 5), key='summative_assignments')]

]
add_assignment_layout = [
    [sg.T('Assignment ID:'), sg.InputText(size=7, key='assignment_id')],
    [sg.T('Grade (x/x):'), sg.InputText(size=4, key='assignment_grade')],
    [sg.T('s/f:'), sg.InputText(size=3, key='assignment_category'), sg.Button('Add')],



]

sf_layout = [
    [sg.Frame('Scaling ', sf_scale_layout), sg.Frame('Add Assignment', add_assignment_layout)],
    [sg.Frame('Formative Assignments', formative_assignments_layout)],
    [sg.Frame('Summative Assignments', summative_assignments_layout)]
]


layout_tab2 = [
    [sg.T('This is inside tab 2')]
    
    
]

layout_tabgroup = [[sg.Tab('Summative/Formative', sf_layout)], [sg.Tab('Tab 2', layout_tab2)]]
layout_frame = [[sg.TabGroup(layout_tabgroup)]]
layout = [
    [sg.Frame('Grade Simulator',layout_frame)],
    [sg.Button('Quit'), sg.Button('Clear'), sg.Button('Export'), sg.Button('Import:'), sg.InputText(key='import_data')]
    ]

def update_assignments_windows():
    formative_element_values=[]
    for x in assignments:
        if assignments[x]['category']=='formative':
            formative_element_values.append (f'{x} | Grade:{assignments[x]["grade"]}/{assignments[x]["max_grade"]}')
    window.Element('formative_assignments').update(formative_element_values)    

    summative_element_values=[]
    for x in assignments:
        if assignments[x]['category']=='summative':
            summative_element_values.append (f'{x} | Grade:{assignments[x]["grade"]}/{assignments[x]["max_grade"]}')
    window.Element('summative_assignments').update(summative_element_values)

def update_scales_windows():
    window.Element('formative_scale').update(formative_scale)
    window.Element('summative_scale').update(summative_scale)

def update_all_windows():
    update_assignments_windows()
    update_scales_windows()

window = sg.Window('Juice', layout)

class InputError(Exception):
    pass

#  window.read(close=True)
while True:
    event, values = window.read()
    #print('values: ',values)

    try:
        if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
            break
        if event == 'Update Scale':
            m_s=re.fullmatch(DECIMAL_PATTERN, values['summative_scale'])
            m_f=re.fullmatch(DECIMAL_PATTERN, values['formative_scale'])
            if m_s is None or m_f is None:
                raise InputError('Invalid scale. Enter an integer or a decimal.')
            summative_scale = float(m_s.group(1))
            formative_scale = float(m_f.group(1))
        if event == 'Export':
            pyperclip.copy(json.dumps(
                {
                    'summative_scale': summative_scale,
                    'formative_scale': formative_scale,
                    'assignments': assignments
                }))

        if event == 'Import:':
            import_data = json.loads(values['import_data'])
            summative_scale = import_data['summative_scale']
            formative_scale = import_data['formative_scale']
            assignments = import_data['assignments']

            update_all_windows()

        if event == 'Add':
            m=re.fullmatch(r'(\d+(?:\.\d*)?)/(\d+(?:\.\d*)?)', values['assignment_grade'])
            if m is None:
                raise InputError('Invalid grade. Make sure it is in the x/y format and try again.')
            if values['assignment_category'] !='f' and values['assignment_category'] !='s':
                raise InputError('Category should be either f or s')
    
            assignments[values['assignment_id']] = {
                'grade' : float(m.group(1)),
                'max_grade' : float(m.group(2)),
                'category' : 'formative' if values['assignment_category'] =='f' else 'summative'
            }
        if event == 'Clear':
            summative_scale =0
            formative_scale =0
            assignments ={}
        update_assignments_windows()                

    except InputError as e:
        sg.popup(e)
    except JSONDecodeError as e:
        sg.popup(f'Invalid import string. Make sure the clipboard gets populated via the Export button.')
    # print('You entered', values)
    

window.close()