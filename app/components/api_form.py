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
        'Spam - Inbound Prospecting (Apollo)': {
            'subject': 'Expert live onboarding + Q&A',
            'from': 'James from Apollo <james@mail.apollo.io>',
            'to': 'roberto.camacho@chapi.cl',
            'date': '2025-09-12T20:56:25Z',
            'body': """
                Hey Roberto,
                
                I'm James, Apollo Academy instructor here at Apollo. Need a hand getting started?
                
                I host daily live onboarding sessions where I teach you the basics of Apollo 
                and answer your questions, and I'd love for you to join me for one.
                
                Folks who attend an onboarding session with me are 80% more likely to book a 
                meeting than those that don't.
                
                Choose a time and sign up here: https://app.apollo.io/?utm_campaign=webinar
                
                See you there!
                
                James O'Sullivan
                Apollo Academy Instructor
                
                ©2025 Apollo. All rights reserved.
                Unsubscribe | Manage preferences
            """,
            'thread': """
                === Mensaje anterior ===
                De: roberto.camacho@chapi.cl
                Fecha: 2025-09-12T15:56:48Z
                
                Re:
            """
        },
        'Conversation Ended - Meeting Reminder': {
            'subject': 'Re: Recordatorio reunión',
            'from': 'begona@cliente.com',
            'to': 'jaime.fuenzalida@welcomeback.io',
            'date': '2025-10-06T09:05:00Z',
            'body': """
                Gracias, nos vemos.
            """,
            'thread': """
                === Mensaje anterior (Manual SDR reminder) ===
                De: jaime.fuenzalida@welcomeback.io
                Fecha: 2025-10-06T09:00:00Z
                
                Hola Begoña,
                
                Solo recordarte nuestra reunión de hoy a las 11:00 hrs. Te comparto 
                nuevamente el link para que nos conectemos: REUNIÓN CON WELCOMEBACK
                http://meet.google.com/hpi-wypo-vts
                
                Quedo atento a cualquier cambio que necesites.
                
                Un abrazo,
                Jaime
            """
        },
        'Rejection - Should NOT Close': {
            'subject': 'Re: Propuesta comercial',
            'from': 'cliente@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T16:00:00Z',
            'body': """
                Catalina,
                
                Gracias por tu interés, pero ya tenemos un proveedor con el que
                estamos muy conformes y no estamos buscando cambiar en este momento.
                
                Te agradecería que no me contactes nuevamente.
                
                Saludos.
            """,
            'thread': """
                === Email anterior ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-01T10:00:00Z
                
                Hola, te contacto para presentarte nuestra solución...
            """
        },
        'Referral - Should NOT Close': {
            'subject': 'Re: Propuesta comercial',
            'from': 'ignacio@empresa.com',
            'to': 'catalina.moraga@influence.cl',
            'date': '2025-07-02T14:00:00Z',
            'body': """
                Hola Catalina,
                
                Yo no soy la persona indicada para esto.
                
                Te sugiero contactar a Daniela López, nuestra Gerente Comercial.
                Su correo es daniela.lopez@empresa.com
                
                Ella podrá ayudarte mejor.
                
                Saludos,
                Ignacio
            """,
            'thread': """
                === Email anterior ===
                De: catalina.moraga@influence.cl
                Fecha: 2025-07-01T10:00:00Z
                
                Hola, te contacto para presentarte nuestra solución...
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


def close_thread_sent_form():
    
    # Example scenarios
    examples = {
        'Close - Meeting Confirmed': {
            'received_subject': 'Re: Propuesta de reunión',
            'received_body': """
                Hola Catalina,
                
                Perfecto! ¿Cuándo tienes disponibilidad para una llamada de 30 minutos?
                Yo estoy libre el martes por la tarde.
                
                Saludos,
                María
            """,
            'sent_to': 'maria.gonzalez@empresaXYZ.com',
            'sent_body': """
                Hola María,
                
                Excelente! Te agendé para el martes 8 de julio a las 15:00 hrs.
                Te llegará la invitación de Google Calendar a este correo.
                
                Cualquier cosa me avisas!
                
                Saludos,
                Catalina
            """,
            'labels': ['AI']
        },
        'Close - Still Proposing (Should NOT Close)': {
            'received_subject': 'Re: Coordinemos reunión',
            'received_body': """
                Hola Catalina,
                
                Me interesa mucho! ¿Cuándo podríamos conversar?
                
                Saludos,
                Pedro
            """,
            'sent_to': 'pedro.ramirez@startup.cl',
            'sent_body': """
                Hola Pedro,
                
                Perfecto! Tengo disponibilidad el miércoles 10 a las 11:00 
                o el jueves 11 a las 16:00.
                
                ¿Cuál te acomoda mejor?
                
                Saludos,
                Catalina
            """,
            'labels': ['AI']
        },
        'Safe - Rejection Acknowledged': {
            'received_subject': 'Re: Propuesta comercial',
            'received_body': """
                Catalina,
                
                Gracias por tu interés, pero ya tenemos un proveedor con el que
                estamos muy conformes y no estamos buscando cambiar.
                
                Saludos.
            """,
            'sent_to': 'director@empresa.com',
            'sent_body': """
                Hola Director,
                
                Entendido, muchas gracias por tu tiempo y honestidad.
                
                Si en algún momento cambian de parecer o necesitan una segunda
                opinión, estaremos encantados de conversar.
                
                ¡Mucho éxito!
                
                Saludos cordiales,
                Catalina
            """,
            'labels': ['AI']
        },
        'Safe - OOO Handled': {
            'received_subject': 'Respuesta automática',
            'received_body': """
                Respuesta automática: Fuera de la oficina
                
                Estaré fuera hasta el 15 de julio sin acceso regular al correo.
                Para asuntos urgentes, contactar a asistente@empresa.com
                
                Saludos,
                Carlos
            """,
            'sent_to': 'carlos.mendez@empresa.com',
            'sent_body': """
                Hola Carlos,
                
                Sin problema! Te contactaré después del 15 de julio.
                
                Que tengas un buen descanso!
                
                Saludos,
                Catalina
            """,
            'labels': ['AI']
        },
        'Convince - Should NOT Close': {
            'received_subject': 'Re: Información sobre servicios',
            'received_body': """
                Hola Catalina,
                
                Suena interesante, pero necesito más información sobre
                los resultados que han logrado con clientes similares.
                
                Saludos,
                Laura
            """,
            'sent_to': 'laura.torres@corporativo.com',
            'sent_body': """
                Hola Laura,
                
                Claro que sí! Te comparto algunos casos de éxito:
                
                1. Cliente A: Incremento de 40% en conversiones
                2. Cliente B: ROI de 3.5x en 6 meses
                3. Cliente C: Reducción de 60% en costo por lead
                
                Te parece si agendamos una llamada para discutir cómo
                podríamos lograr resultados similares para ustedes?
                
                Quedo atenta!
                
                Saludos,
                Catalina
            """,
            'labels': ['AI']
        },
        'Referral - Should NOT Close': {
            'received_subject': 'Re: Oportunidad de colaboración',
            'received_body': """
                Hola Catalina,
                
                Yo no soy la persona indicada para esto.
                Te sugiero contactar a Daniela López, nuestra Gerente Comercial.
                Su correo es daniela.lopez@empresa.com
                
                Saludos,
                Juan
            """,
            'sent_to': 'juan.perez@empresa.com',
            'sent_body': """
                Hola Juan,
                
                Muchas gracias por la referencia!
                
                Le escribiré directamente a Daniela López.
                Te agradezco mucho la ayuda!
                
                Saludos,
                Catalina
            """,
            'labels': ['AI']
        },
        'Safe - Bounce (Error Handled)': {
            'received_subject': 'Mail Delivery Failed',
            'received_body': """
                Delivery Status Notification (Failure)
                
                This is an automatically generated Delivery Status Notification.
                Delivery to the following recipients failed:
                contacto@empresa-inexistente.com
                Reason: 550 User unknown
            """,
            'sent_to': 'contacto@empresa-inexistente.com',
            'sent_body': '',
            'labels': ['BOUNCE']
        }
    }
    
    # Example selector before the form
    example_key = st.selectbox(
        'Select Example Scenario (Sent Message)',
        list(examples.keys()),
        index=0,
        help='Choose a pre-loaded example to test different sent message scenarios',
        key='sent_example_selector'
    )
    
    selected_example = examples[example_key]
    
    with st.form('close_thread_sent_form'):

        st.subheader('Close Thread (Sent) Test Input')

        received_subject = st.text_input('Received Subject', value=selected_example['received_subject'])
        received_body = st.text_area(
            'Received Body',
            height=120,
            value=clean_body(selected_example['received_body'])
        )
        sent_to = st.text_input('Sent To', value=selected_example['sent_to'])
        sent_body = st.text_area(
            'Sent Body (Our Response)',
            height=200,
            value=clean_body(selected_example['sent_body'])
        )
        labels_input = st.text_input('Labels (comma-separated)', value=', '.join(selected_example['labels']))
        
        submitted = st.form_submit_button('Test Close Thread (Sent) API')

        # Parse labels
        labels = [label.strip() for label in labels_input.split(',') if label.strip()]

        return submitted, {
            'received_subject': received_subject,
            'received_body': clean_body(received_body),
            'sent_to': sent_to,
            'sent_body': clean_body(sent_body),
            'labels': labels
        }


def create_meeting_form():
    
    # Example scenarios for creating meetings
    examples = {
        'Meeting with María González - EnterpriseXYZ': {
            'from': 'catalina.moraga@influence.cl',
            'to': 'maria.gonzalez@empresaXYZ.com',
            'meeting_date': '2025-07-08T15:00:00',
            'seller': 'catalina.moraga@influence.cl',
            'thread': """
                === Mensaje 1 (Inicial) ===
                De: catalina.moraga@influence.cl
                Para: maria.gonzalez@empresaXYZ.com
                Fecha: 2025-07-01T10:00:00Z
                Asunto: Propuesta de reunión
                
                Hola María,
                
                Gracias por tu interés en nuestros servicios de marketing digital.
                ¿Cuándo tendrías disponibilidad para una llamada de 30 minutos?
                
                Tenemos slots el martes 8 a las 3 PM o el miércoles 9 a las 10 AM.
                
                Saludos,
                Catalina Moraga
                Influence Marketing
                
                === Mensaje 2 ===
                De: maria.gonzalez@empresaXYZ.com
                Para: catalina.moraga@influence.cl
                Fecha: 2025-07-02T09:00:00Z
                Asunto: Re: Propuesta de reunión
                
                Hola Catalina,
                
                ¡Perfecto! El martes 8 a las 3 PM me viene genial.
                Soy Gerente de Marketing en EnterpriseXYZ y estoy muy 
                interesada en conocer cómo pueden ayudarnos.
                
                Mi celular es +56 9 8765 4321 por si necesitan contactarme.
                
                Nos vemos entonces!
                
                Saludos,
                María González
                Gerente de Marketing
                EnterpriseXYZ
                
                === Mensaje 3 (Confirmación) ===
                De: catalina.moraga@influence.cl
                Para: maria.gonzalez@empresaXYZ.com
                Fecha: 2025-07-02T14:30:00Z
                Asunto: Re: Propuesta de reunión
                
                Excelente María! 
                
                Te confirmo la reunión para el martes 8 de julio a las 15:00 hrs.
                Te llegará la invitación de Google Calendar a este correo.
                Juan Pérez también participará de la reunión.
                
                Cualquier cosa me avisas!
                
                Saludos,
                Catalina
            """
        },
        'Meeting with Pedro Ramírez - StartupCL': {
            'from': 'catalina.moraga@influence.cl',
            'to': 'pedro.ramirez@startup.cl',
            'meeting_date': '2025-07-10T11:00:00',
            'seller': 'catalina.moraga@influence.cl',
            'thread': """
                === Mensaje 1 ===
                De: pedro.ramirez@startup.cl
                Para: catalina.moraga@influence.cl
                Fecha: 2025-07-05T16:00:00Z
                Asunto: Consulta sobre servicios
                
                Hola,
                
                Me llamo Pedro Ramírez, soy CEO de StartupCL. 
                Estamos buscando una agencia que nos ayude con marketing digital.
                
                ¿Tienen experiencia con startups en etapa temprana?
                
                Saludos,
                Pedro
                
                === Mensaje 2 ===
                De: catalina.moraga@influence.cl
                Para: pedro.ramirez@startup.cl
                Fecha: 2025-07-05T17:30:00Z
                Asunto: Re: Consulta sobre servicios
                
                Hola Pedro!
                
                Claro que sí, tenemos bastante experiencia con startups.
                ¿Te parece si coordinamos una llamada para conversar más?
                
                Tengo disponibilidad:
                - Miércoles 10 a las 11:00
                - Jueves 11 a las 16:00
                
                Saludos,
                Catalina
                
                === Mensaje 3 ===
                De: pedro.ramirez@startup.cl
                Para: catalina.moraga@influence.cl
                Fecha: 2025-07-06T10:00:00Z
                Asunto: Re: Consulta sobre servicios
                
                Perfecto! El miércoles 10 a las 11:00 me viene bien.
                
                Nos vemos entonces!
                Pedro
            """
        },
        'Meeting with Laura Torres - Corporativo (with phone)': {
            'from': 'juan.perez@influence.cl',
            'to': 'laura.torres@corporativo.com',
            'meeting_date': '2025-07-12T14:30:00',
            'seller': 'juan.perez@influence.cl',
            'thread': """
                === Mensaje 1 ===
                De: juan.perez@influence.cl
                Para: laura.torres@corporativo.com
                Fecha: 2025-07-08T09:00:00Z
                Asunto: Propuesta de consultoría de marketing
                
                Hola Laura,
                
                Somos Influence, una agencia de marketing digital especializada
                en empresas corporativas. Me gustaría conversar contigo sobre
                cómo podemos ayudar a Corporativo con su estrategia digital.
                
                ¿Tendrías disponibilidad para una llamada?
                
                Saludos,
                Juan Pérez
                Influence
                
                === Mensaje 2 ===
                De: laura.torres@corporativo.com
                Para: juan.perez@influence.cl
                Fecha: 2025-07-08T15:00:00Z
                Asunto: Re: Propuesta de consultoría de marketing
                
                Hola Juan,
                
                Me interesa conocer más. ¿Cuándo podrían?
                
                Saludos,
                Laura Torres
                Directora de Marketing Digital
                Corporativo SA
                +56 2 3456 7890
                
                === Mensaje 3 ===
                De: juan.perez@influence.cl
                Para: laura.torres@corporativo.com
                Fecha: 2025-07-09T10:00:00Z
                Asunto: Re: Propuesta de consultoría de marketing
                
                Hola Laura,
                
                Perfecto! Te propongo:
                - Viernes 12 a las 14:30
                - Lunes 15 a las 10:00
                
                ¿Cuál te acomoda mejor?
                
                Saludos,
                Juan
                
                === Mensaje 4 ===
                De: laura.torres@corporativo.com
                Para: juan.perez@influence.cl
                Fecha: 2025-07-09T16:00:00Z
                Asunto: Re: Propuesta de consultoría de marketing
                
                El viernes 12 a las 14:30 está perfecto.
                
                Nos vemos!
                Laura
            """
        },
        'Meeting with Josefa González - Quintec (detailed info)': {
            'from': 'catalina.moraga@influence.cl',
            'to': 'josefa.gonzalez@quintec.cl',
            'meeting_date': '2025-07-09T10:00:00',
            'seller': 'catalina.moraga@influence.cl',
            'thread': """
                === Mensaje 1 ===
                De: josefa.gonzalez@quintec.cl
                Para: catalina.moraga@influence.cl
                Fecha: 2025-07-02T10:30:00Z
                Asunto: ¿Podemos agendar 20 minutos?
                
                Hola Catalina,

                Dentro de Quintec trabajo como Encargada de Marketing de BackOnline.
                Esta es nuestra web para que nos conozcas www.backonline.cl.

                Encantada de agendar una reunión para conocer cómo trabajan. 
                
                Tengo disponibilidad el próximo lunes a las 10:00 o martes a las 15:00.
                ¿Te acomoda alguno de estos horarios?

                Saludos,
                Josefa González
                Encargada de Marketing - BackOnline
                Quintec
                josefa.gonzalez@quintec.cl
                +56 9 1234 5678
                
                === Mensaje 2 ===
                De: catalina.moraga@influence.cl
                Para: josefa.gonzalez@quintec.cl
                Fecha: 2025-07-02T14:00:00Z
                Asunto: Re: ¿Podemos agendar 20 minutos?
                
                Hola Josefa!
                
                Claro que sí! El lunes 9 a las 10:00 me viene perfecto.
                Te enviaré la invitación de calendario.
                
                Saludos,
                Catalina
            """
        }
    }
    
    # Example selector before the form
    example_key = st.selectbox(
        'Select Example Scenario',
        list(examples.keys()),
        index=0,
        help='Choose a pre-loaded example to test the create meeting flow',
        key='create_meeting_example_selector'
    )
    
    selected_example = examples[example_key]
    
    with st.form('create_meeting_form'):

        st.subheader('Create Meeting Test Input')

        from_email = st.text_input('From (Inbox)', value=selected_example['from'])
        to_email = st.text_input('To (Prospect Email)', value=selected_example['to'])
        meeting_date = st.text_input('Meeting Date (ISO format)', value=selected_example['meeting_date'])
        seller = st.text_input('Seller', value=selected_example['seller'])
        thread = st.text_area(
            'Email Thread',
            height=300,
            value=clean_body(selected_example['thread']),
            help='Full email thread where the meeting was confirmed'
        )

        submitted = st.form_submit_button('Test Create Meeting API')

        return submitted, {
            'sdr_email': from_email,
            'prospect_email': to_email,
            'meeting_date': meeting_date,
            'seller': seller,
            'thread': clean_body(thread)
        }
