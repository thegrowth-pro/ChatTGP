# app/components/api_form.py

import streamlit as st

import textwrap

def api_form():
    
    # Example scenarios for each strategy
    examples = {
        'Close - Accept Meeting': {
            'subject': 'Re: Propuesta de reunión',
            'from': 'maria.gonzalez@empresaXYZ.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T09:15:00Z',
            'body': """
                Hola Catalina,
                
                Perfecto! Me interesa mucho conocer más sobre sus servicios.
                
                ¿Cuándo tienes disponibilidad para una llamada de 30 minutos?
                Yo estoy libre el martes o miércoles por la tarde.
                
                Saludos,
                María
            """
        },
        'Close - Propose Times': {
            'subject': '¿Podemos agendar 20 minutos?',
            'from': 'josefa.gonzalez@quintec.cl',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T10:30:00Z',
            'body': """
                Hola Catalina,

                Dentro de Quintec trabajo como encargada de marketing de BackOnline.
                Esta es nuestra web para que nos conozcas www.backonline.cl.

                Encantada de agendar una reunión para conocer cómo trabajan. 
                
                Tengo disponibilidad el próximo lunes a las 10:00 o martes a las 15:00.
                ¿Te acomoda alguno de estos horarios?

                Saludos.
            """
        },
        'Close - CC/Forward': {
            'subject': 'Re: Información sobre servicios',
            'from': 'roberto.silva@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T14:00:00Z',
            'body': """
                Hola Catalina,
                
                Te copio a Ana Martínez (ana.martinez@empresa.com), nuestra Gerente 
                de Marketing. Ella es quien toma las decisiones en este tema.
                
                Ana, Catalina puede ayudarnos con nuestras campañas digitales.
                ¿Podrías coordinar una reunión con ella?
                
                Saludos,
                Roberto
            """
        },
        'Convince - Ask for Info': {
            'subject': 'Re: Propuesta de marketing digital',
            'from': 'pedro.ramirez@startup.cl',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T11:00:00Z',
            'body': """
                Hola Catalina,
                
                Gracias por contactarnos. Suena interesante, pero necesito entender
                mejor cómo funcionan sus servicios.
                
                ¿Tienen casos de éxito con startups de nuestro tamaño? ¿Podrían
                enviarme información sobre los resultados que han logrado?
                
                También me gustaría saber los rangos de inversión aproximados.
                
                Quedo atento,
                Pedro
            """
        },
        'Convince - Request Materials': {
            'subject': 'Re: Servicios de consultoría',
            'from': 'laura.torres@corporativo.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T15:30:00Z',
            'body': """
                Catalina,
                
                Me interesa pero necesito presentar esto a mi equipo directivo.
                
                ¿Podrías enviarme un PDF con su propuesta comercial, casos de éxito
                y un benchmark comparativo con la competencia?
                
                Con eso podré agendar una reunión más adelante.
                
                Gracias!
            """
        },
        'Referral - Wrong Contact': {
            'subject': 'Re: Oportunidad de colaboración',
            'from': 'juan.perez@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T12:00:00Z',
            'body': """
                Hola Catalina,
                
                Yo no soy la persona indicada para esto. 
                
                Te sugiero contactar a Daniela López, nuestra Gerente Comercial.
                Su correo es daniela.lopez@empresa.com
                
                Ella podrá ayudarte mejor.
                
                Saludos,
                Juan
            """
        },
        'Referral - Forward Internally': {
            'subject': 'Re: Consulta sobre servicios',
            'from': 'admin@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T16:00:00Z',
            'body': """
                Hola,
                
                He reenviado tu correo al área de Marketing.
                Ellos se pondrán en contacto contigo directamente.
                
                Saludos cordiales.
            """
        },
        'Safe - Out of Office': {
            'subject': 'Respuesta automática',
            'from': 'carlos.mendez@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T08:00:00Z',
            'body': """
                Respuesta automática: Fuera de la oficina
                
                Estaré fuera hasta el 15 de julio sin acceso regular al correo.
                
                Para asuntos urgentes, favor contactar a mi asistente:
                asistente@empresa.com
                
                Saludos,
                Carlos Méndez
            """
        },
        'Safe - Rejection': {
            'subject': 'Re: Propuesta comercial',
            'from': 'director@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T13:00:00Z',
            'body': """
                Catalina,
                
                Gracias por tu interés, pero ya tenemos un proveedor con el que
                estamos muy conformes y no estamos buscando cambiar en este momento.
                
                Te agradecería que no me contactes nuevamente.
                
                Saludos.
            """
        },
        'Safe - Spam/Bounce': {
            'subject': 'Mail Delivery Failed',
            'from': 'MAILER-DAEMON@mail.example.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T10:00:00Z',
            'body': """
                Delivery Status Notification (Failure)
                
                This is an automatically generated Delivery Status Notification.
                
                Delivery to the following recipients failed:
                
                contacto@empresa-inexistente.com
                
                Reason: 550 User unknown
            """
        }
    }
    
    # Example selector before the form
    example_key = st.selectbox(
        'Select Example Scenario',
        list(examples.keys()),
        index=0,
        help='Choose a pre-loaded example to test different classification strategies'
    )
    
    selected_example = examples[example_key]
    
    with st.form('api_form'):

        st.subheader('Classification Test Input')

        subject = st.text_input('Subject', value=selected_example['subject'])
        sender = st.text_input('From', value=selected_example['from'])
        recipient = st.text_input('To', value=selected_example['to'])
        date = st.text_input('Date', value=selected_example['date'])
        body = st.text_area(
            'Body',
            height=220,
            value=clean_body(selected_example['body'])
        )

        submitted = st.form_submit_button('Test Classification API')

        return submitted, {
            'subject': subject,
            'from_': sender,
            'to': recipient,
            'date': date,
            'body': clean_body(body)
        }

def clean_body(body: str) -> str:
    return textwrap.dedent(body).strip()


def close_thread_form():
    
    # Example scenarios
    examples = {
        'Meeting Confirmed': {
            'subject': 'Re: Reunión confirmada',
            'from': 'maria.gonzalez@empresaXYZ.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T14:30:00Z',
            'body': """
                Perfecto Catalina, confirmado para el martes 5 de julio a las 3 PM.
                
                Nos vemos entonces!
                
                Saludos,
                María
            """,
            'thread': """
                === Mensaje 1 (Inicial) ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-01T10:00:00Z
                
                Hola María, gracias por tu interés. Tenemos disponibilidad el martes 5 
                a las 3 PM o el miércoles 6 a las 10 AM. ¿Cuál te acomoda mejor?
                
                === Mensaje 2 ===
                De: maria.gonzalez@empresaXYZ.com
                Fecha: 2025-07-02T09:00:00Z
                
                Hola Catalina, el martes a las 3 PM me viene perfecto!
                
                === Mensaje 3 (Anterior) ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-02T09:30:00Z
                
                Excelente, te envío la invitación al calendario.
            """
        },
        'Bounce': {
            'subject': 'Mail Delivery Failed',
            'from': 'MAILER-DAEMON@mail.example.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T10:15:00Z',
            'body': """
                This is an automatically generated Delivery Status Notification.
                
                Delivery to the following recipients failed permanently:
                
                   maria.gonzalez@empresaXYZ.com
                
                Reason: 550 User unknown
            """,
            'thread': """
                === Mensaje Original ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-02T10:00:00Z
                
                Hola María, gracias por tu interés en coordinar una reunión...
            """
        },
        'Spam': {
            'subject': '🎁 OFERTA EXCLUSIVA - No te lo pierdas!',
            'from': 'ofertas@marketing-blast.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T12:00:00Z',
            'body': """
                ¡OFERTA LIMITADA! ¡SOLO HOY!
                
                Increíbles descuentos en nuestros productos premium.
                Click aquí: http://suspicious-link.com/offer
                
                Este email fue enviado a 50,000+ destinatarios.
                
                Para desuscribirte, haz click aquí.
            """,
            'thread': ''
        },
        'Unsubscribe Request': {
            'subject': 'Re: Newsletter semanal',
            'from': 'cliente@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T16:00:00Z',
            'body': """
                Hola,
                
                Por favor elimíname de tu lista de correos. No me interesa 
                recibir más información.
                
                Gracias.
            """,
            'thread': """
                === Email anterior ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-01T10:00:00Z
                
                Newsletter semanal con novedades...
            """
        },
        'Ongoing Conversation': {
            'subject': 'Re: Información sobre servicios',
            'from': 'prospecto@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T11:00:00Z',
            'body': """
                Hola Catalina,
                
                Gracias por la información. Me interesa mucho, pero necesito 
                revisar el presupuesto con mi equipo. ¿Podrías enviarme también 
                algunos casos de éxito de clientes similares?
                
                Saludos,
            """,
            'thread': """
                === Mensaje Inicial ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-01T14:00:00Z
                
                Hola, te envío información sobre nuestros servicios...
            """
        }
    }
    
    # Example selector before the form
    example_key = st.selectbox(
        'Select Example Scenario',
        list(examples.keys()),
        index=0,
        help='Choose a pre-loaded example to test different close thread scenarios'
    )
    
    selected_example = examples[example_key]
    
    with st.form('close_thread_form'):

        st.subheader('Close Thread Test Input')

        subject = st.text_input('Subject', value=selected_example['subject'])
        sender = st.text_input('From', value=selected_example['from'])
        recipient = st.text_input('To', value=selected_example['to'])
        date = st.text_input('Date', value=selected_example['date'])
        body = st.text_area(
            'Body (Latest Message)',
            height=150,
            value=clean_body(selected_example['body'])
        )
        thread = st.text_area(
            'Thread (Previous Messages)',
            height=200,
            value=clean_body(selected_example['thread'])
        )

        submitted = st.form_submit_button('Test Close Thread API')

        return submitted, {
            'subject': subject,
            'from_': sender,
            'to': recipient,
            'date': date,
            'body': clean_body(body),
            'thread': clean_body(thread)
        }
