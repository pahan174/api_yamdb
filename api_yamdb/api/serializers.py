from rest_framework import serializers
from reviews.models import Genre, Category, Title
from users.models import CustomUser
from reviews.models import Review, Comment


class SignUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        ref_name = 'ReadOnlyUsers'

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" использовать нельзя.'
            )
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class GetPersonalAccountSerializers(serializers.ModelSerializer):
    username = serializers.StringRelatedField()
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        if instance.role != CustomUser.ADMIN:
            attrs['role'] = instance.role
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    token = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = (
            'username', 'confirmation_code', 'token'
        )

    def validate(self, attrs):
        if not attrs.get('username'):
            raise ValueError('Введите имя пользователя.')
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        fields = ('id', 'score', 'author', 'text', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if not self.partial and Review.objects.filter(title__id=title_id,
                                                      author=author).exists():
            raise serializers.ValidationError('Нельзя оставить отзыв дважды!')
        return data


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitlesSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year', 'description')
        model = Title


class TitleDetailSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    genre = GenreSerializer(
        many=True, read_only=True)

    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'category', 'genre', 'name', 'year', 'description', 'rating')
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment
