import azure.functions as func
import logging
import socks
import socket
import asyncpg
import os

app = func.FunctionApp()

@app.function_name(name="HttpTrigger1")
@app.route(route="netbird", auth_level=func.AuthLevel.ANONYMOUS)
async def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Set up the SOCKS5 proxy
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(os.getenv('NB_SOCKS5_LISTENER_PORT', '1080')))
    socket.socket = socks.socksocket

    conn = await asyncpg.connect(user=os.getenv('POSTGRES_USER', 'postgres'),
                                 password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
                                 database=os.getenv('POSTGRES_DB', 'postgres'),
                                 host=os.getenv('POSTGRES_HOST', '127.0.0.1'))

    # Get the visitor's IP address
    visitor_ip = req.headers.get('X-Forwarded-For')

    # Insert the visit into the database
    await conn.execute("INSERT INTO visits (ip_address) VALUES ($1)", visitor_ip)

    # Retrieve the last 10 visits
    visits = await conn.fetch("SELECT ip_address, visit_time FROM visits ORDER BY visit_time DESC LIMIT 10")
    # Close the database connection
    await conn.close()
    # Format the visit history
    visit_history = "Latest endpoint access log:\n" + "\n".join([f"SourceIP: {ip}, Time: {time}" for ip, time in visits])

    # Return the visit history
    return func.HttpResponse(visit_history, mimetype="text/plain")