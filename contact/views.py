from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.mail import send_mail, mail_admins
from django.template.loader import render_to_string
from django.conf import settings

from .models import Contact
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_form = form.save()
            mail_recd = Contact.objects.get(id=contact_form.id)
            name = mail_recd.name

            # Send "message rec'd mail"
            cust_email = mail_recd.email
            subject = render_to_string(
                'contact/confirmation_emails/mail_recd_subject.txt',
                {'mail_recd': mail_recd})
            body = render_to_string(
                'contact/confirmation_emails/mail_recd_body.txt',
                {'mail_recd': mail_recd,
                    'contact_email': settings.DEFAULT_FROM_EMAIL})
            # Send mail to admin
            admin_subject = render_to_string(
                'contact/confirmation_emails/admin_mail_recd_subject.txt',
                {'mail_recd': mail_recd})
            admin_body = render_to_string(
                'contact/confirmation_emails/admin_mail_recd_body.txt',
                {'mail_recd': mail_recd,
                    'contact_email': settings.DEFAULT_FROM_EMAIL})

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email],
                fail_silently=True,
            )

            mail_admins(
                admin_subject,
                admin_body,
            )
            messages.success(request, 'We have received your message. Thanks!')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'We did not receive your message. Please \
                make sure the form is valid')
            return redirect(reverse('contact', args=[contact_form.id]))

    else:
        form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contact/contact.html', context)


