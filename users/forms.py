from django import forms
from django.core.exceptions import ValidationError
from .models import CreateUser, Create_subs
from django.utils.translation import gettext_lazy as _
import re
class UserForm(forms.ModelForm):
    """
    Formulario avanzado para registro de usuarios con validaciones personalizadas.
    Incluye campos personalizados y mensajes de error específicos.
    """
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa una contraseña segura',
            'autocomplete': 'new-password'
        }),
        help_text='Al menos 6 caracteres, combina letras y números.'
    )
    
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'autocomplete': 'new-password'
        })
    )
    
    cumpleaños = forms.DateTimeField(
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'max': '2005-01-01'  # Limita la edad a ~18 años
        })
    )
    
    nickname = forms.CharField(
        label='Nickname',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre en juegos',
            'maxlength': '20'
        })
    )
    
    edad = forms.IntegerField(
        label='Edad',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu edad actual',
            'min': '18',
            'max': '99'
        })
    )

    celular = forms.CharField(
        label='Número de teléfono',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu número de teléfono',
            'maxlength': '20'
        }),
        required=True  # Asegúrate de que sea obligatorio
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu email'
        })
    )

    class Meta:
        model = CreateUser
        fields = [
            'username', 'password', 'password_confirm', 'first_name',
            'nickname', 'edad', 'cumpleaños', 'pais', 'ciudad', 
            'celular',  # Asegúrate de incluir el campo celular aquí
            'juego_principal', 'reclutado_por'
        ]
        
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre real',
            'pais': 'País',
            'ciudad': 'Ciudad',
            'juego_principal': 'Juego principal',
            'reclutado_por': 'Reclutado por'
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario único'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre real'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu país de residencia'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu ciudad'
            }),
           
            'juego_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu juego principal'
            }),
            'reclutado_por': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        
        error_messages = {
            'username': {
                'required': 'El nombre de usuario es obligatorio.',
                'invalid': 'El formato del nombre de usuario no es válido.',
                'unique': 'Este nombre de usuario ya está en uso.'
            },
            'cumpleaños': {
                'required': 'La fecha de nacimiento es obligatoria.',
                'invalid': 'La fecha ingresada no es válida.'
            },
            'first_name': {
                'required': 'Tu nombre real es obligatorio.',
                'max_length': 'El nombre es demasiado largo.'
            },
            'pais': {
                'required': 'Debes indicar tu país.'
            },
            'ciudad': {
                'required': 'Debes indicar tu ciudad.'
            }
        }
        
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        # Configuración global de mensajes de error
        for field_name, field in self.fields.items():
            field.error_messages.update({
                'required': f'El campo {self.fields[field_name].label} es obligatorio.',
                'invalid': f'El valor ingresado para {self.fields[field_name].label} no es válido.'
            })
            
            # Marcar todos los campos como obligatorios
            if field_name not in ['hobby']:
                field.required = True

    def clean_username(self):
        """Validar que el nombre de usuario sea único y tenga formato válido."""
        username = self.cleaned_data.get('username')
        
        if not username:
            raise ValidationError("El nombre de usuario es obligatorio.")
            
        if len(username) < 3:
            raise ValidationError("El nombre de usuario debe tener al menos 3 caracteres.")
            
        if CreateUser.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso. Por favor elige otro.")
            
        return username

    def clean_password(self):
        """Validar requisitos de seguridad de la contraseña."""
        password = self.cleaned_data.get('password')
        
        if len(password) < 6:
            raise ValidationError("La contraseña debe tener al menos 6 caracteres.")
            
        if password.isdigit():
            raise ValidationError("La contraseña no puede contener solo números.")
            
        return password

    def clean_password_confirm(self):
        """Validar que las contraseñas coincidan."""
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
            
        return password_confirm
        
    def clean_email(self):
        """Validar que el email sea único y tenga formato válido."""
        email = self.cleaned_data.get('email')
        
        if not email:
            raise ValidationError("El email es obligatorio.")
            
        if CreateUser.objects.filter(email=email).exists():
            raise ValidationError("Este email ya está en uso. Por favor elige otro.")
            
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            raise ValidationError("El formato del email no es válido.")
        if len(email) > 254:
            raise ValidationError("El email no puede tener más de 254 caracteres.")

        return email

    def clean_edad(self):
        """Validar que el usuario tenga al menos 18 años."""
        edad = self.cleaned_data.get('edad')
        
        if not edad:
            raise ValidationError("La edad es obligatoria.")
            
        if edad < 18 or edad > 99:
            raise ValidationError("La edad debe estar entre 18 y 99 años.")
            
        return edad

    def clean_cumpleaños(self):
        """Validar que la fecha de cumpleaños sea válida."""
        cumpleaños = self.cleaned_data.get('cumpleaños')
        
        if not cumpleaños:
            raise ValidationError("La fecha de nacimiento es obligatoria.")
            
        return cumpleaños
        
    def clean_celular(self):
        """Validar que el número de celular sea válido."""
        celular = self.cleaned_data.get('celular')
        
        if not celular:
            raise ValidationError("El número de teléfono es obligatorio.")
        
        # Aquí puedes agregar más validaciones si es necesario (por ejemplo, formato)
        
        return celular
        
    def clean(self):
        """Validaciones cruzadas entre campos."""
        cleaned_data = super().clean()
        
        # Ejemplo de validación cruzada: verificar que la edad coincida con la fecha de nacimiento
        edad = cleaned_data.get('edad')
        cumpleaños = cleaned_data.get('cumpleaños')
        
        if edad and cumpleaños:
            # Aquí podrías implementar una validación más compleja si lo deseas
            pass
            
        return cleaned_data
        
    def save(self, commit=True):
        """Guardar el usuario con contraseña encriptada y crear perfil."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            
            # Crear perfil automáticamente (si es necesario)
            try:
                from .models import Perfil
                Perfil.objects.get_or_create(
                    user=user,
                    defaults={
                        'nickname': user.nickname,
                        'nivel': 1,
                        'puntos_exp': 0,
                        'puntos_honor': 0,
                        'xp_siguiente_nivel': 100
                    }
                )
            except Exception as e:
                # Solo registrar el error, pero permitir que el usuario se cree
                print(f"Error al crear perfil: {e}")
                
        return user
        
  