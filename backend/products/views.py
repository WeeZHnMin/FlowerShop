from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
import requests
import json
import base64
from PIL import Image
from io import BytesIO
from openai import OpenAI
import datetime

from .models import Flower, Post, Comment, Like
from .serializers import FlowerSerializer, PostSerializer, CommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'owner'

class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer
    permission_classes = [IsOwnerOrReadOnly]

class RecognizeFlowerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=400)

        try:
            pil_img = Image.open(image_file)
            buffer = BytesIO()
            pil_img.save(buffer, format='JPEG', quality=85)
            compressed_image_data = buffer.getvalue()
        except Exception as e:
            return Response({"error": f"Invalid image file: {e}"}, status=400)

        try:
            with open('config.json') as config_file:
                config = json.load(config_file)
                access_token = config.get("access_token")
        except (FileNotFoundError, json.JSONDecodeError):
            return Response({"error": "Access token not configured"}, status=500)

        url = f"https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={access_token}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {"image": base64.b64encode(compressed_image_data)}

        try:
            response = requests.post(url, data=params, headers=headers)
            response.raise_for_status()
            recognition_result = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to call recognition API: {e}"}, status=500)

        if "result" in recognition_result and recognition_result["result"]:
            best_guess = recognition_result["result"][0]["name"]
            matching_flowers = Flower.objects.filter(name__icontains=best_guess)
            serializer = FlowerSerializer(matching_flowers, many=True)
            return JsonResponse({
                'recognized_name': best_guess,
                'matching_flowers': serializer.data
            })
        else:
            return JsonResponse({'recognized_name': '无法识别', 'matching_flowers': []})

class AskQwenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response({"error": "No question provided"}, status=400)

        try:
            from django.conf import settings
            import os
            config_path = os.path.join(settings.BASE_DIR, 'config.json')
            with open(config_path) as config_file:
                config = json.load(config_file)
                api_key = config.get("QWEN_API_KEY")
        except (FileNotFoundError, json.JSONDecodeError):
            return Response({"error": "API key not configured"}, status=500)

        if not api_key:
            return Response({"error": "QWEN_API_KEY not found in config.json"}, status=500)

        client = OpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        def event_stream():
            try:
                stream = client.chat.completions.create(
                    model="qwen-plus",
                    messages=[
                        {"role": "system", "content": "你是一个专业的花卉顾问，具备丰富的花卉养护和花艺搭配知识。请根据用户的提问执行以下职责：1. 如果用户提出花卉养护相关问题（如浇水、光照、施肥、换盆等），请提供具体、实用的建议。2. 如果用户描述了病虫害症状（如叶子发黄、黑斑、虫蛀等），请判断可能的原因，并推荐对应的药品或处理方法。3. 如果用户输入的是常见生活场景（如婚庆、葬礼、探病、家居装饰等），请根据场景推荐适合的花卉品种，展示方式要简洁明了、便于客户选择。4. 如无法识别问题，请引导用户提供更多信息。"},
                        {"role": "user", "content": question},
                    ],
                    stream=True,
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content or ""
                    yield f"data: {json.dumps({'choices': [{'delta': {'content': content}}]})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

class LogJsonErrorView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        error_data = request.data
        with open("frontend-errors.txt", "a", encoding="utf-8") as f:
            f.write(f"--- Error Logged at {datetime.datetime.now()} ---\n")
            f.write(json.dumps(error_data, indent=2, ensure_ascii=False))
            f.write("\n\n")
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def likes(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
