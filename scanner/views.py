from django.shortcuts import render
import cv2
from pyzbar.pyzbar import decode
import time
from django.http import HttpResponse,StreamingHttpResponse,JsonResponse
import threading
from django.views.decorators import gzip
from .forms import BarcodeForm, ScanCode
from .models import Scan,Shelf
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView,UpdateView,FormView
from django.urls import reverse_lazy
import numpy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.urls import reverse
# Create your views here.

class AddShelf(CreateView):
    model = Shelf
    fields = ['shelf']
    template_name = 'scanner/add_shelf.html'
    success_url = reverse_lazy('scanner:shelf')

    def form_valid(self,model):
        request = self.request
        messages.add_message(request, messages.SUCCESS, 'SHELF ADDED SUCCESSFULLY!')
        return super().form_valid(model)

class Shelves(ListView):
    model = Shelf
    template_name  = 'scanner/home.html'


class ShelfDetailAdd(DetailView):
    model  = Shelf
    template_name = 'scanner/shelf_add_detail.html'
    success_url = reverse_lazy("scanner:shelf")

    def get_context_data(self, **kwargs):
        context = super(ShelfDetailAdd, self).get_context_data(**kwargs)
        context['form'] = ScanCode
        return context

    def post(self, request, *args, **kwargs):
        form = ScanCode(request.POST, request.FILES)
        if form.is_valid():
            request= self.request
            # Write Your Logic here
            shelf = request.POST.get('shelf')
            print("Shelf", shelf)
            image = form.cleaned_data.get('barcode')
            qty = form.cleaned_data.get('qty')
            manual_code = form.cleaned_data.get('barcode_manually')
            shelf_id = Shelf.objects.get(shelf=shelf).id
            # print(qty)
            if manual_code:
                obj = Scan.objects.filter(code=manual_code,shelf=shelf)
                if obj:
                    stock = Scan.objects.get(code=manual_code).qty
                    stock = stock + qty
                    obj = Scan.objects.filter(code=manual_code).update(qty=stock)
                    messages.add_message(request, messages.INFO, 'Stock updated successfully!')
                    return redirect(reverse("scanner:shelf_details", kwargs = {'pk':shelf_id}))
                elif not obj:
                    obj = Scan.objects.create(shelf=shelf,code=manual_code,qty=qty)
                    obj.save()
                    messages.add_message(request, messages.SUCCESS, 'STOCK ADDED SUCCESSFULLY!')
                    return redirect(reverse("scanner:shelf_details", kwargs = {'pk':shelf_id}))
            if image:
                img1 = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                # cv2.imshow(img)
                print("DECODED",len(decode(img)))
                if len(decode(img)) == 0:
                    messages.add_message(request, messages.ERROR, 'CODE HAD NO DATA, PLEASE TRY AGAIN!')
                    return redirect(reverse("scanner:shelf_details", kwargs = {'pk':shelf_id}))
                else:
                    for code in decode(img):
                        print(code.data.decode("utf-8"))
                        print(code.type)

                        if not code.data.decode("utf-8"):
                            print("No Data!")
                            messages.add_message(request, messages.ERROR, 'BARCODE COULD NOT BE READ, PLEASE TRY AGAIN!')
                        else:
                            obj = Scan.objects.filter(code=code.data.decode("utf-8"),shelf=shelf)
                            if obj:
                                stock = Scan.objects.get(code=code.data.decode("utf-8")).qty
                                stock = stock + qty
                                obj = Scan.objects.filter(code=code.data.decode("utf-8")).update(qty=stock)
                                messages.add_message(request, messages.INFO, 'Stock updated successfully!')
                                return redirect(reverse("scanner:shelf_details", kwargs = {'pk':shelf_id}))
                            elif not obj:
                                obj = Scan.objects.create(shelf=shelf,code=code.data.decode("utf-8"),qty=qty)
                                obj.save()
                                messages.add_message(request, messages.SUCCESS, 'STOCK ADDED SUCCESSFULLY!')
                                return redirect(reverse("scanner:shelf_details", kwargs = {'pk':shelf_id}))
            self.object = self.get_object()
            context = super(ShelfDetailAdd, self).get_context_data(**kwargs)
            context['form'] =  ScanCode
            return self.render_to_response(context=context)

        else:
            self.object = self.get_object()
            context = super(ShelfDetailAdd, self).get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response( context=context)





def readBarcode(request):

    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    camera = True

    used_codes = []



    while camera == True:
        success, frame = cap.read()

        for code in decode(frame):
            if code.data.decode('utf-8') not in used_codes:
                print("Approved")
                print(code.type)
                print(code.data.decode('utf-8'))
                used_codes.append(code.data.decode('utf-8'))
                time.sleep(5)
            elif code.data.decode('utf-8') in used_codes:
                print("CODE ALREADY SCANNED!")
                time.sleep(5)



        cv2.imshow("testing", frame)
        cv2.waitKey(1)
        # video = {
        #     "cap":cap,
        #     "img":img,
        #
        # }
        # return render(request,'scanner/test.html',video)

# class ReadImage(CreateView):
#     form_class = BarcodeForm
#     model = Scan
#     template_name = 'scanner/upload.html'
#     success_url = reverse_lazy('scanner:upload')
#     def form_valid(self,form):
#         request = self.request
#         image = form.cleaned_data.get('image')
#         qty = form.cleaned_data.get('qty')
#
#         print(image)
#         img = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
#
#         print(decode(img))
#
#         return super().form_valid(form)

def read_image(request):
    form = ScanCode()
    if request.method == "POST":
        form = ScanCode(request.POST,request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('barcode')
            qty = form.cleaned_data.get('qty')
            manual_code = form.cleaned_data.get('barcode_manually')
            # print(qty)
            if manual_code:
                obj = Scan.objects.filter(code=manual_code)
                if obj:
                    stock = Scan.objects.get(code=manual_code).qty
                    stock = stock + qty
                    obj = Scan.objects.filter(code=manual_code).update(qty=stock)
                    messages.add_message(request, messages.INFO, 'Stock updated successfully!')
                    return redirect("scanner:upload")
                elif not obj:
                    obj = Scan.objects.create(code=manual_code,qty=qty)
                    obj.save()
                    messages.add_message(request, messages.SUCCESS, 'STOCK ADDED SUCCESSFULLY!')
                    return redirect("scanner:upload")
            if image:
                img1 = cv2.imdecode(numpy.fromstring(image.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                print("DECODED",len(decode(img)))
                if len(decode(img)) == 0:
                    messages.add_message(request, messages.ERROR, 'CODE HAD NO DATA, PLEASE TRY AGAIN!')
                    return redirect("scanner:upload")
                else:
                    for code in decode(img):
                        print(code.data.decode("utf-8"))
                        print(code.type)

                        if not code.data.decode("utf-8"):
                            print("No Data!")
                            messages.add_message(request, messages.ERROR, 'BARCODE COULD NOT BE READ, PLEASE TRY AGAIN!')
                        else:
                            obj = Scan.objects.filter(code=code.data.decode("utf-8"))
                            if obj:
                                stock = Scan.objects.get(code=code.data.decode("utf-8")).qty
                                stock = stock + qty
                                obj = Scan.objects.filter(code=code.data.decode("utf-8")).update(qty=stock)
                                messages.add_message(request, messages.INFO, 'Stock updated successfully!')
                                return redirect("scanner:upload")
                            elif not obj:
                                obj = Scan.objects.create(code=code.data.decode("utf-8"),qty=qty)
                                obj.save()
                                messages.add_message(request, messages.SUCCESS, 'STOCK ADDED SUCCESSFULLY!')
                                return redirect("scanner:upload")
    return render(request, 'scanner/upload.html',{"form":form})


@gzip.gzip_page
def scan_now(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return render(request, 'scanner/scan.html')


    return render(request,'scanner/scan.html',{})

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
         self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
