class PagesController < ApplicationController
  def home
  end

  # def show
  #   @languages = Language.all
  #   @label = Label.find_by(id: params[:id].to_i)

  #   # _____________________________________________________________Label Made In
  #   @labelmadein = []

  #   # Sucht Sprachen Ids fuer Kunden
  #   customer_lang = MadeInLanguage.where(customer_id: @label.customer_id)
  #   customer_lang_ids = []
  #   customer_lang.each { |l| customer_lang_ids << l.language_id }

  #   # Findet alle MadeIn mit entsprechemdem Sprache (alle Tags)
  #   a = []

  #   customer_lang_ids.each do |id|
  #     MadeIn.all.each do |made|
  #       a << made if id == made.language_id
  #     end
  #   end

  #   # Sucht alle MadIn mit entsprechendem Tag raus
  #   label_made_in_tag = MadeIn.find_by(id: @label.made_in_id).tag

  #   a.each do |made|
  #     @labelmadein << made.text if label_made_in_tag == made.tag
  # end

end

