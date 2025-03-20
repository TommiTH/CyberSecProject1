from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect

from .models import Choice, Question

import logging
import datetime

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #-------------- FIX FOR FLAW 1: -----------------------------------------------
    #if not request.user.is_authenticated:
    #    redirect("/polls")
    #    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    #------------------------------------------------------------------------------
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Flaw 5, no logging. Logging has been setup in the settings file, 
        # so now in here we can start logging votes and hopefully stop a very possible election fraud.
        #time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        #logger.warning(str(request.user.username) + " voted. \n  Question_id: " + str(question_id) + " , Selected: " + str(selected_choice) + "\n  " + time)
        #------------------------------------------------------------------------
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
