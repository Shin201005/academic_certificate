from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student

        fields = [
            "id",
            "school",
            "user",
            "student_code",
            "full_name",
            "date_of_birth",
            "email",
        ]

        read_only_fields = [
            "id",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        if request is None:
            return attrs

        current_user = request.user

        if not current_user.is_authenticated:
            raise serializers.ValidationError(
                "Ban chua dang nhap."
            )

        if current_user.role == "SCHOOL":
            if current_user.school_id is None:
                raise serializers.ValidationError(
                    "Tai khoan chua duoc gan truong."
                )

            school = attrs.get("school")

            if school is not None:
                if school.id != current_user.school_id:
                    raise serializers.ValidationError({
                        "school": (
                            "Khong duoc gan sinh vien "
                            "vao truong khac."
                        )
                    })

            if self.instance is not None:
                if self.instance.school_id != current_user.school_id:
                    raise serializers.ValidationError(
                        "Khong duoc sua sinh vien truong khac."
                    )

        school = attrs.get("school")

        if school is None and self.instance is not None:
            school = self.instance.school

        student_code = attrs.get("student_code")

        if student_code is None and self.instance is not None:
            student_code = self.instance.student_code

        if school is not None and student_code is not None:

            queryset = Student.objects.filter(
                school=school,
                student_code=student_code
            )

            if self.instance is not None:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise serializers.ValidationError({
                    "student_code": (
                        "Ma sinh vien da ton tai "
                        "trong truong nay."
                    )
                })

        linked_user = attrs.get("user")

        if linked_user is None and self.instance is not None:
            linked_user = self.instance.user

        if linked_user is not None:
            if linked_user.role != "STUDENT":
                raise serializers.ValidationError({
                    "user": "Tai khoan lien ket phai co vai tro STUDENT."
                })

            if school is not None and linked_user.school_id != school.id:
                raise serializers.ValidationError({
                    "user": "Tai khoan khong thuoc truong cua sinh vien."
                })

        return attrs