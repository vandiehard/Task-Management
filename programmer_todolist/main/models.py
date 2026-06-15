from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class ProgrammerProfile(models.Model):
    SKILL_CHOICES = [
        ('python', 'Python'), ('javascript', 'JavaScript'), ('php', 'PHP'),
        ('java', 'Java'), ('cpp', 'C++'), ('csharp', 'C#'), ('go', 'Go'),
        ('rust', 'Rust'), ('swift', 'Swift'), ('kotlin', 'Kotlin'),
        ('ruby', 'Ruby'), ('typescript', 'TypeScript'), ('dart', 'Dart'),
        ('html', 'HTML'), ('css', 'CSS'), ('react', 'React'), ('vue', 'Vue.js'),
        ('angular', 'Angular'), ('nodejs', 'Node.js'), ('laravel', 'Laravel'),
        ('django', 'Django'), ('flask', 'Flask'), ('nextjs', 'Next.js'),
        ('svelte', 'Svelte'),
        ('react_native', 'React Native'), ('flutter', 'Flutter'),
        ('mysql', 'MySQL'), ('postgresql', 'PostgreSQL'), ('mongodb', 'MongoDB'),
        ('redis', 'Redis'), ('firebase', 'Firebase'),
        ('docker', 'Docker'), ('kubernetes', 'Kubernetes'), ('aws', 'AWS'),
        ('git', 'Git'),
        ('machine_learning', 'Machine Learning'), ('data_science', 'Data Science'),
        ('rest_api', 'REST API'), ('graphql', 'GraphQL'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    skills = models.JSONField(default=list, help_text="Selected programming skills")
    is_available = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"

    def get_skills_display(self):
        skill_dict = dict(self.SKILL_CHOICES)
        return [skill_dict.get(skill, skill) for skill in self.skills]

    def get_skills_badges(self):
        skill_dict = dict(self.SKILL_CHOICES)
        return [{'code': skill, 'name': skill_dict.get(skill, skill)} for skill in self.skills]


class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    assigned_to = models.ForeignKey(ProgrammerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'project_id': self.pk})

    def save(self, *args, **kwargs):
        if self.assigned_to and self.status == 'assigned':
            self.assigned_to.is_available = False
            self.assigned_to.save()
        super().save(*args, **kwargs)


class ProjectSubmission(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/')
    notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approval_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Submission for {self.project.title}"
