from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404

from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text_from_pdf
from .summarizer import summarize_text
from .contract_parser import extract_contract_info
from .risk_analyzer import (
    analyze_risks,
    summarize_risks,
    calculate_risk_score,
)


# ============================================================
# WEB PAGE - UPLOAD AND ANALYZE DOCUMENT
# ============================================================

def upload_document(request):

    context = {
        "documents": Document.objects.all().order_by("-uploaded_at")
    }

    if request.method == "POST":

        title = request.POST.get("title")
        uploaded_file = request.FILES.get("file")

        # ----------------------------------------------------
        # Validate title
        # ----------------------------------------------------
        if not title:
            context["message"] = "Title is missing."

        # ----------------------------------------------------
        # Validate file
        # ----------------------------------------------------
        elif not uploaded_file:
            context["message"] = "Please choose a PDF."

        # ----------------------------------------------------
        # Validate PDF extension
        # ----------------------------------------------------
        elif not uploaded_file.name.lower().endswith(".pdf"):
            context["message"] = "Only PDF files are allowed."

        else:

            try:
                # ------------------------------------------------
                # 1. Save document
                # ------------------------------------------------
                document = Document.objects.create(
                    title=title,
                    file=uploaded_file
                )

                # ------------------------------------------------
                # 2. Extract text from PDF
                # ------------------------------------------------
                text = extract_text_from_pdf(
                    document.file.path
                )

                if not text or not text.strip():

                    document.delete()

                    context["message"] = (
                        "Could not extract text from this PDF."
                    )

                    return render(
                        request,
                        "homepage.html",
                        context
                    )

                # ------------------------------------------------
                # 3. Generate summary
                # ------------------------------------------------
                summary = summarize_text(text)

                # ------------------------------------------------
                # 4. Analyze risks
                # ------------------------------------------------
                risks = analyze_risks(text)

                # ------------------------------------------------
                # 5. Generate risk summary
                # ------------------------------------------------
                risk_summary = summarize_risks(risks)

                # ------------------------------------------------
                # 6. Calculate risk score
                # ------------------------------------------------
                risk_score = calculate_risk_score(risks)

                # ------------------------------------------------
                # 7. Extract contract information
                # ------------------------------------------------
                contract_info = extract_contract_info(text)

                # ------------------------------------------------
                # 8. Save results to database
                # ------------------------------------------------
                document.extracted_text = text
                document.summary = summary
                document.risk_score = risk_score["score"]
                document.risk_level = risk_score["level"]

                document.save()

                # ------------------------------------------------
                # 9. Send results to frontend
                # ------------------------------------------------
                context["message"] = (
                    "Document analyzed successfully!"
                )

                context["summary"] = summary
                context["risks"] = risks
                context["risk_summary"] = risk_summary
                context["risk_score"] = risk_score
                context["contract_info"] = contract_info
                context["extracted_text"] = text

                # Refresh document list
                context["documents"] = (
                    Document.objects.all()
                    .order_by("-uploaded_at")
                )

            except Exception as e:

                # Print complete error in PyCharm terminal
                import traceback
                traceback.print_exc()

                context["message"] = (
                    f"Error while analyzing document: {str(e)}"
                )

    return render(
        request,
        "homepage.html",
        context
    )


# ============================================================
# REST API - DOCUMENT UPLOAD
# ============================================================

class DocumentUploadView(APIView):

    def get(self, request):

        documents = Document.objects.all().order_by("-uploaded_at")

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = DocumentSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # ------------------------------------------------
            # 1. Save uploaded document
            # ------------------------------------------------
            document = serializer.save()

            # ------------------------------------------------
            # 2. Extract text
            # ------------------------------------------------
            extracted_text = extract_text_from_pdf(
                document.file.path
            )

            if not extracted_text or not extracted_text.strip():

                document.delete()

                return Response(
                    {
                        "error": "Could not extract text from this PDF."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ------------------------------------------------
            # 3. Analyze risks
            # ------------------------------------------------
            risks = analyze_risks(extracted_text)

            # ------------------------------------------------
            # 4. Risk summary
            # ------------------------------------------------
            risk_summary = summarize_risks(risks)

            # ------------------------------------------------
            # 5. Calculate risk score
            # ------------------------------------------------
            risk_score = calculate_risk_score(risks)

            # ------------------------------------------------
            # 6. Generate summary
            # ------------------------------------------------
            summary = summarize_text(extracted_text)

            # ------------------------------------------------
            # 7. Extract contract information
            # ------------------------------------------------
            contract_info = extract_contract_info(
                extracted_text
            )

            # ------------------------------------------------
            # 8. Save everything
            # ------------------------------------------------
            document.extracted_text = extracted_text
            document.summary = summary
            document.risk_score = risk_score["score"]
            document.risk_level = risk_score["level"]

            document.save()

            # ------------------------------------------------
            # 9. Return API response
            # ------------------------------------------------
            return Response(
                {
                    "message": (
                        "Document uploaded and analyzed successfully."
                    ),
                    "data": DocumentSerializer(document).data,
                    "summary": summary,
                    "risks": risks,
                    "risk_summary": risk_summary,
                    "risk_score": risk_score,
                    "contract_info": contract_info,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            import traceback
            traceback.print_exc()

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================================
# DOCUMENT DETAILS PAGE
# ============================================================

def document_detail(request, document_id):

    document = get_object_or_404(
        Document,
        id=document_id
    )

    # --------------------------------------------------------
    # Make sure extracted text exists
    # --------------------------------------------------------
    if document.extracted_text:

        risks = analyze_risks(
            document.extracted_text
        )

        risk_summary = summarize_risks(
            risks
        )

        contract_info = extract_contract_info(
            document.extracted_text
        )

    else:

        risks = []
        risk_summary = {}
        contract_info = {}

    # --------------------------------------------------------
    # Risk score
    # --------------------------------------------------------
    risk_score = {
        "score": document.risk_score,
        "level": document.risk_level
    }

    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------
    context = {
        "document": document,
        "summary": document.summary,
        "risks": risks,
        "risk_summary": risk_summary,
        "risk_score": risk_score,
        "contract_info": contract_info,
        "extracted_text": document.extracted_text,
    }

    return render(
        request,
        "document_detail.html",
        context
    )