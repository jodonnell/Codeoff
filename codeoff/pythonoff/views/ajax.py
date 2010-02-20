from django.shortcuts import render_to_response

def send_buffer(request):
    return render_to_response('index.html', {})
