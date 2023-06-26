from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import (Category, Genre, GenreTitle,
                            Title, User, Review, Comments)
from users.validators import validate_username


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data

    def validated_unique_review(self, attrs):
        title = attrs['title']
        author = self.context['request'].user

        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError("Отзыв существует уже")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', 'author')


class TitleSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанров."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='review_title__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = GenreTitle


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя."""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    email = serializers.EmailField(max_length=254,)

    def validate(self, data):
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if (User.objects.filter(username=data['username']).exists()
                or User.objects.filter(email=data['email']).exists()):
            raise serializers.ValidationError(
                'Пользователь с такими данными уже существует!'
            )
        return data

    class Meta:
        model = User
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, ]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )
