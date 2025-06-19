package models

import (
	"time"
	"github.com/google/uuid"
)

type WikiPage struct {
	BaseModel
	Title       string    `json:"title" gorm:"not null"`
	Slug        string    `json:"slug" gorm:"uniqueIndex;not null"`
	Content     string    `json:"content" gorm:"type:text"`
	ProjectID   uuid.UUID `json:"project_id" gorm:"not null"`
	AuthorID    uuid.UUID `json:"author_id" gorm:"not null"`
	IsPublished bool      `json:"is_published" gorm:"default:false"`
	Version     int       `json:"version" gorm:"default:1"`
	ParentID    *uuid.UUID `json:"parent_id"` // Para jerarquía de páginas
	
	// Metadata
	Tags        []string               `json:"tags" gorm:"type:jsonb"`
	Metadata    map[string]interface{} `json:"metadata" gorm:"type:jsonb"`
	
	// Relaciones
	Project    *Project       `json:"project,omitempty"`
	Author     *User          `json:"author,omitempty"`
	Parent     *WikiPage      `json:"parent,omitempty"`
	Children   []WikiPage     `json:"children,omitempty" gorm:"foreignKey:ParentID"`
	Revisions  []WikiRevision `json:"revisions,omitempty"`
	Comments   []WikiComment  `json:"comments,omitempty"`
	
	// Timestamps adicionales
	PublishedAt *time.Time `json:"published_at"`
	LastEditedAt time.Time `json:"last_edited_at" gorm:"default:CURRENT_TIMESTAMP"`
}

type WikiRevision struct {
	BaseModel
	PageID    uuid.UUID `json:"page_id" gorm:"not null"`
	Title     string    `json:"title" gorm:"not null"`
	Content   string    `json:"content" gorm:"type:text"`
	AuthorID  uuid.UUID `json:"author_id" gorm:"not null"`
	Version   int       `json:"version" gorm:"not null"`
	Summary   string    `json:"summary"` // Resumen de cambios
	
	// Relaciones
	Page   *WikiPage `json:"page,omitempty"`
	Author *User     `json:"author,omitempty"`
}

type WikiComment struct {
	BaseModel
	Content  string    `json:"content" gorm:"not null"`
	PageID   uuid.UUID `json:"page_id" gorm:"not null"`
	UserID   uuid.UUID `json:"user_id" gorm:"not null"`
	ParentID *uuid.UUID `json:"parent_id"`
	
	// Relaciones
	Page    *WikiPage     `json:"page,omitempty"`
	User    *User         `json:"user,omitempty"`
	Parent  *WikiComment  `json:"parent,omitempty"`
	Replies []WikiComment `json:"replies,omitempty" gorm:"foreignKey:ParentID"`
}

type WikiAttachment struct {
	BaseModel
	PageID   uuid.UUID `json:"page_id" gorm:"not null"`
	FileName string    `json:"file_name" gorm:"not null"`
	FileURL  string    `json:"file_url" gorm:"not null"`
	FileSize int64     `json:"file_size"`
	MimeType string    `json:"mime_type"`
	
	// Relación
	Page *WikiPage `json:"page,omitempty"`
}

type CreateWikiPageRequest struct {
	Title       string                 `json:"title" binding:"required,min=2,max=200"`
	Content     string                 `json:"content"`
	ParentID    *uuid.UUID             `json:"parent_id"`
	IsPublished bool                   `json:"is_published"`
	Tags        []string               `json:"tags"`
	Metadata    map[string]interface{} `json:"metadata"`
}

type UpdateWikiPageRequest struct {
	Title       string                 `json:"title,omitempty" binding:"omitempty,min=2,max=200"`
	Content     string                 `json:"content,omitempty"`
	IsPublished *bool                  `json:"is_published,omitempty"`
	Tags        []string               `json:"tags,omitempty"`
	Summary     string                 `json:"summary"` // Resumen de cambios
	Metadata    map[string]interface{} `json:"metadata,omitempty"`
}

type WikiPageFilter struct {
	IsPublished *bool    `json:"is_published" form:"is_published"`
	AuthorID    *uuid.UUID `json:"author_id" form:"author_id"`
	ParentID    *uuid.UUID `json:"parent_id" form:"parent_id"`
	Search      string   `json:"search" form:"search"`
	Tags        []string `json:"tags" form:"tags"`
}

func (wp *WikiPage) GenerateSlug() string {
	// TODO: Implementar generación de slug a partir del título
	return "wiki-page-slug"
}

func (wp *WikiPage) CanBeEditedBy(userID uuid.UUID, userRole UserRole) bool {
	if userRole == RoleAdmin || userRole == RoleManager {
		return true
	}
	
	return wp.AuthorID == userID
}

func (wp *WikiPage) CanBeViewedBy(userID uuid.UUID, projectMember bool) bool {
	if wp.IsPublished {
		return projectMember
	}
	
	// Solo el autor puede ver páginas no publicadas
	return wp.AuthorID == userID
}

func (wp *WikiPage) CreateRevision(authorID uuid.UUID, summary string) *WikiRevision {
	return &WikiRevision{
		PageID:   wp.ID,
		Title:    wp.Title,
		Content:  wp.Content,
		AuthorID: authorID,
		Version:  wp.Version,
		Summary:  summary,
	}
}
