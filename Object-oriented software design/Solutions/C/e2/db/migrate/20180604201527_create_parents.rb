class CreateParents < ActiveRecord::Migration[5.1]
  def change
    create_table :parents do |t|
      t.integer :my_id

      t.timestamps
    end
  end
end
