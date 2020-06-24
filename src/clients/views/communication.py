class EditClientCommunicationFrequencyView(LoginRequiredMixin, generic.UpdateView):
    template_name = "clients/edit_details.html"
    model = ClientCommunicationFrequency
    fields = ('face_to_face_frequency', 'calls_frequency', 
    'email_frequency','sms_frequency')
    
    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save
        
        messages.add_message(
            self.request, messages.SUCCESS, "client communication frequency successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditClientCommunicationFrequencyView, self).form_valid(form)
