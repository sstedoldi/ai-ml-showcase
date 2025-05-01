def hide(class_id):
    return '''<style>
    %(class_id)s 
    {
        visibility: hidden;    
    }
    </style>''' % {"class_id": class_id}

def sidebar():
    return '''<style>
    .st-emotion-cache-a6qe2i 
    {
        padding: 0px 1.5rem 1.5rem;;    
    }
    </style>'''

def lg_color(class_id):
    return '''<style>
    %(class_id)s
    {
        background-image: linear-gradient(90deg, rgb(88, 110, 118), rgb(173, 216, 230));   
    }
    </style>''' % {"class_id": class_id}

def cont_padding(class_id):
    return '''<style>
    %(class_id)s
    {
        padding: 16px;
    }
    </style>''' % {"class_id": class_id}