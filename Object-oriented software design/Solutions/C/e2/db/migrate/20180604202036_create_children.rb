class CreateChildren < ActiveRecord::Migration[5.1]
  def change
    create_table :children do |t|
      t.integer :my_id
      t.integer :par_id

      t.timestamps
    end
  end
end
