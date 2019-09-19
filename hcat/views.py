from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
import json

from .models import *

# Create your views here (except API views go in api.py)

def index(request):
    a = []
    for p in Project.objects.order_by("-id"):
        j = {"short_name":p.short_name, "title":p.title}
        a.append(j)
    return HttpResponse(json.dumps(a), content_type="application/json")

def api_index(request):
    objects = [Project, ProjectState, Contributor, Tracker, AssayTech, Disease, Organ]
    a = []
    for o in objects:
        p = {"class": o.__name__, "count": o.objects.count()}
        a.append(p)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_assay_tech(c):
    projects = []
    for p in c.projects.all():
         projects.append(p.short_name)
    return {"short_name": c.short_name, "description": c.description, "projects": projects}

def api_assaytech_list(request):
    a = []
    for p in AssayTech.objects.order_by("id"):
        j = serializable_assay_tech(p)
        a.append(j)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_project_state(p):
    return {"state": p.state, "description": p.description}

def api_projectstate_list(request):
    a = []
    for p in ProjectState.objects.order_by("id"):
        j = serializable_project_state(p)
        a.append(j)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_contributor(c):
    projects = []
    for p in c.projects.all():
         projects.append(p.short_name)
    labs = []
    for p in c.labs.all():
         labs.append(p.short_name)
    return {"name": c.name, "type": str(c.type),
            "email": c.email, "phone": c.phone, "address": c.address,
            "department": c.department, "institute":c.institute, "city":c.city,
            "zip_postal_code":c.zip_postal_code, "country":c.country,
            "projects":projects, "labs":labs}
    #projects = models.ManyToManyField("Project", blank=True, through="project_contributors")
    #labs = models.ManyToManyField("Lab", blank=True, through="lab_contributors")
    #grants = models.ManyToManyField("Grant", blank=True, through="grant_funded_contributors")

def api_contributor_list(request):
    a = []
    for p in Contributor.objects.order_by("name"):
        c = serializable_contributor(p)
        a.append(c)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_organ(c):
    projects = []
    for p in c.projects.all():
         projects.append(p.short_name)
    return {"short_name": c.short_name, "description": c.description, "projects":projects}

def api_organ_list(request):
    a = []
    for p in Organ.objects.order_by("short_name"):
        c = serializable_organ(p)
        a.append(c)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_tracker(c):
    return {
        "project": str(c.project),
        "uuid": c.uuid, "submission_id": c.submission_id, 
        "submission_bundles_exported_count":c.submission_bundles_exported_count, 
        "aws_primary_bundle_count":c.aws_primary_bundle_count,
        "gcp_primary_bundle_count":c.gcp_primary_bundle_count,
        "aws_analysis_bundle_count":c.aws_analysis_bundle_count,
        "gcp_analysis_bundle_count":c.gcp_analysis_bundle_count,
        "azul_analysis_bundle_count":c.azul_analysis_bundle_count,
        "succeeded_workflows":c.succeeded_workflows,
        "matrix_bundle_count":c.matrix_bundle_count,
        "matrix_cell_count":c.matrix_cell_count,
        }

def api_tracker_list(request):
    a = []
    for p in Tracker.objects.order_by("-project_id"):
        c = serializable_tracker(p)
        a.append(c)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_disease(c):
    projects = []
    for p in c.projects.all():
         projects.append(p.short_name)
    return {"short_name": c.short_name, "description": c.description, "projects":projects}

def api_disease_list(request):
    a = []
    for p in Disease.objects.order_by("short_name"):
        c = serializable_disease(p)
        a.append(c)
    return HttpResponse(json.dumps(a), content_type="application/json")

def serializable_project(p):
    contributors = []
    for c in p.contributors.all():
        contributors.append(str(c))
    organs = []
    for o in p.organ.all():
        organs.append(str(o))
    species = []
    for s in p.species.all():
        species.append(str(s))
    return {
        "short_name":p.short_name, "stars":p.stars, "cur_state": str(p.cur_state), 
        "origin_name": p.origin_name, "title":p.title, 
        "wrangler1": str(p.wrangler1), "wrangler2": str(p.wrangler2), 
        "species":species, "organs":organs, "contributors":contributors,
        "description":p.description, "submit_date":str(p.submit_date)}
    
def api_project_list(request):
    a = []
    for p in Project.objects.order_by("-id"):
        j = serializable_project(p)
        a.append(j)
    return HttpResponse(json.dumps(a), content_type="application/json")


class ProjectListView(generic.ListView):
    template_name = 'hcat/project_list.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.order_by("-id")[:100]
    
class ProjectDetailView(generic.DetailView):
    model=Project
    template_name = 'hcat/project_detail.html'
    context_object_name = 'project'

