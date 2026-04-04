package services

import (
	"deteleng-backend/internal/config"
	"deteleng-backend/internal/models"
	"deteleng-backend/internal/repository"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

type AuthService struct {
	repo      repository.Repository
	jwtSecret string
}

func NewAuthService(repo repository.Repository) *AuthService {
	cfg := config.Load()
	return &AuthService{
		repo:      repo,
		jwtSecret: cfg.JWTSecret,
	}
}

func NewAuthServiceOnly(cfg *config.Config) *AuthService {
	return &AuthService{
		jwtSecret: cfg.JWTSecret,
	}
}

type Claims struct {
	UserID string `json:"user_id"`
	Email  string `json:"email"`
	Role   string `json:"role"`
	jwt.RegisteredClaims
}

func (s *AuthService) GetUserByEmail(email string) (*models.User, error) {
	return s.repo.GetUserByEmail(email)
}

func (s *AuthService) CreateUser(email, password, role string) (*models.User, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	user := &models.User{
		Email:    email,
		Password: string(hashedPassword),
		Role:     "user",
	}

	if role != "" {
		user.Role = role
	}

	if err := s.repo.CreateUser(user); err != nil {
		return nil, err
	}

	return user, nil
}

func (s *AuthService) LoginByPassword(password string) (string, error) {
	validPassword := password == "novicarsAdminPass" || password == "admin123"
	
	if !validPassword {
		return "", fmt.Errorf("invalid password")
	}

	token, err := s.GenerateToken("admin")
	if err != nil {
		return "", err
	}

	return token, nil
}

func (s *AuthService) GenerateToken(role string) (string, error) {
	claims := Claims{
		UserID: "admin_1",
		Role:   role,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(30 * 24 * time.Hour)), // 30 дней
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(s.jwtSecret))
}

func (s *AuthService) ValidateToken(tokenString string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(s.jwtSecret), nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, jwt.ErrSignatureInvalid
	}

	if claims.ExpiresAt.Before(time.Now()) {
		return nil, jwt.ErrTokenExpired
	}

	return claims, nil
}
