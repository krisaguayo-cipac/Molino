---
layout: default
title: Contact
permalink: /contact/
---

# Contact

You can contact me via email:

- Email: [you@yourdomain.com](mailto:you@yourdomain.com)

Or use the simple form below (Formspree example). To use Formspree:
1. Sign up at https://formspree.io and get your form endpoint (looks like https://formspree.io/f/{id}).
2. Replace the action URL below with your Formspree endpoint.

<form action="https://formspree.io/f/REPLACE_WITH_YOUR_ID" method="POST">
  <label>
    Your name
    <br>
    <input type="text" name="name" required>
  </label>
  <br><br>
  <label>
    Your email
    <br>
    <input type="email" name="_replyto" required>
  </label>
  <br><br>
  <label>
    Message
    <br>
    <textarea name="message" rows="5" required></textarea>
  </label>
  <br><br>
  <button type="submit">Send</button>
</form>

Notes:
- GitHub Pages cannot run server-side code; Formspree posts the form and forwards it to your email.
- If you prefer no external service, remove the form and keep a simple mailto link instead.
