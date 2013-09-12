# Create your views here.

from celery.result import AsyncResult

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json

from youtubetomp3.jobs import download

def index(request):
	return render(request, 'youtubetomp3/index.html')

def poll_state(request):
    """ A view to report the progress to the user """
    if 'job' in request.GET:
        job_id = request.GET['job']
    else:
        return HttpResponse('No job id given.')

    job = AsyncResult(job_id)
    data = job.result or job.state

    return HttpResponse(json.dumps(data), mimetype='application/json')

def init_work(request):
    """ A view to start a background job """
    if 'youtubeLink' in request.POST:
    	job = download.delay(request.POST['youtubeLink'], request.user)
        
    return HttpResponse(job)

def profile(request):
    """ A profile view """
    # if 'profile' in request.GET:
    #     profile = User.objects.get(id=int(request.GET['profile']))
    # else:
    #     return HttpResponse('No profile id given')

    template = loader.get_template('youtubetomp3/profiles/profile_detail.html')
    context = RequestContext(request)

    return HttpResponse(template.render(context))
