class QuestionsController < ApplicationController

  def index
    @question = Question.first
    @answers = Answer.where(question_id: @question.id)
  end

  def show
    @answer_id = params[:id]
    p answer = Answer.find_by(id: @answer_id)

    p Question.find_by(tag: answer.next_question_tag)

    @question = Question.find_by(tag: answer.next_question_tag)
    @answers = Answer.where(question_id: @question.id)
  end


end
