from rest_framework import serializers

from .models import Student
from schools.models import School


class StudentSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all(),
        required=False
    )

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

        read_only_fields = ["id"]

        extra_kwargs = {
            "school": {"required": False},
        }
        validators = []

    def validate(self, attrs):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Ban chua dang nhap."
            )

        current_user = request.user

        if current_user.role not in ("ADMIN", "SCHOOL"):
            raise serializers.ValidationError(
                "Ban khong co quyen quan ly sinh vien."
            )

        school = attrs.get("school")

        # SCHOOL chi duoc quan ly sinh vien cua truong minh
        if current_user.role == "SCHOOL":

            if current_user.school_id is None:
                raise serializers.ValidationError(
                    "Tai khoan chua duoc gan truong."
                )

            if (
                school is not None
                and school.id != current_user.school_id
            ):
                raise serializers.ValidationError({
                    "school": "Khong duoc chon truong khac."
                })

            if (
                self.instance is not None
                and self.instance.school_id != current_user.school_id
            ):
                raise serializers.ValidationError(
                    "Khong duoc sua sinh vien truong khac."
                )

            school = School.objects.get(
                pk=current_user.school_id
            )

        # ADMIN phai chon truong khi tao sinh vien
        elif school is None:

            if self.instance is not None:
                school = self.instance.school
            else:
                raise serializers.ValidationError({
                    "school": "Bat buoc chon truong."
                })

        # SCHOOL khong duoc doi truong so huu
        if current_user.role == "SCHOOL":
            attrs["school"] = school

        # Kiem tra ma sinh vien
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

        # Kiem tra tai khoan lien ket
        linked_user = attrs.get("user")

        if "user" not in attrs and self.instance is not None:
            linked_user = self.instance.user

        if linked_user is not None:

            if linked_user.role != "STUDENT":
                raise serializers.ValidationError({
                    "user": (
                        "Tai khoan phai co vai tro STUDENT."
                    )
                })

            if linked_user.school_id != school.id:
                raise serializers.ValidationError({
                    "user": (
                        "Tai khoan khong thuoc truong "
                        "cua sinh vien."
                    )
                })

        return attrs