from email_engine.link_extractor import extract_portal_links

# Simulate a typical recruiter email body
sample_email = """
Hi Hemant, 
Thanks for applying to Turing! 
You can track your status here: https://turing.com/dashboard/12345
Also, check our greenhouse page: https://hiring.greenhouse.io/p/job123
"""

links = extract_portal_links(sample_email)
print(f"🔗 Found Links: {links}")