# app/components/api_form.py

import streamlit as st

import textwrap

def api_form():
    with st.form('api_form'):

        st.subheader('Test Input')

        subject = st.text_input('Subject', value='¿Podemos agendar 20 minutos?')
        sender = st.text_input('From', value='maria.gonzalez@empresaXYZ.com')
        recipient = st.text_input('To', value='catalina.moraga@influence.cl')
        date = st.text_input('Date', value='2025-07-02T09:15:00Z')
        body = st.text_area(
            'Body',
            height=220,
            value=textwrap.dedent("""
                Hola Belén,

                Cómo estás?

                Dentro de Quintec trabajo como encargada de marketing de BackOnline. Esta
                es nuestra web para que nos conozcas www.backonline.cl.

                Encantada de agendar una reunión para conocer cómo trabajan. Mi Mail
                corporativo es Josefa.gonzalezg@quintec.cl, escríbeme para coordinar.

                Puedo solo el próximo lunes.

                Saludos.
            """).strip()
        )

        submitted = st.form_submit_button('Test API')

        return submitted, {
            'subject': subject,
            'from_': sender,
            'to': recipient,
            'date': date,
            'body': clean_body(body)
        }

def clean_body(body: str) -> str:
    return textwrap.dedent(body).strip()
